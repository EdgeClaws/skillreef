#!/usr/bin/env python3
import sys, os, re, hashlib, pathlib, json

data_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
persist_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/.openclaw/chroma/knowledge-search")
collection_name = sys.argv[3] if len(sys.argv) > 3 else "knowledge"
ollama_url = sys.argv[4] if len(sys.argv) > 4 else "http://localhost:11434"
model_name = sys.argv[5] if len(sys.argv) > 5 else "nomic-embed-text"
chunk_size = int(sys.argv[6]) if len(sys.argv) > 6 else 1500
chunk_overlap = int(sys.argv[7]) if len(sys.argv) > 7 else 200

import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

ef = OllamaEmbeddingFunction(model_name=model_name, url=ollama_url, timeout=120)
client = chromadb.PersistentClient(path=persist_dir)
collection = client.get_or_create_collection(name=collection_name, embedding_function=ef)

MANIFEST_PATH = os.path.join(persist_dir, "ingest_state.json")
FORCE_REINGEST = os.environ.get("FORCE_REINGEST", "0") == "1"

def load_manifest():
    try:
        with open(MANIFEST_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_manifest(manifest):
    tmp = MANIFEST_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(manifest, f)
    os.replace(tmp, MANIFEST_PATH)

def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].strip()
    return text

def extract_title(text):
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            fm = text[3:end]
            m = re.search(r"^title:\s*(.+)$", fm, re.MULTILINE)
            if m:
                return m.group(1).strip().strip("'\"")
    return None

# nomic-embed-text has an 8192 token context window.
# URLs, hashes, and non-English text can tokenize at ~1 char/token,
# so we cap at 2000 chars to stay safely within the limit.
MAX_CHUNK_CHARS = 2000

def hard_split(text, limit):
    """Force-split text that exceeds the embedding model context window."""
    pieces = []
    while len(text) > limit:
        cut = text.rfind(" ", 0, limit)
        if cut <= 0:
            cut = limit
        pieces.append(text[:cut].strip())
        text = text[cut:].strip()
    if text:
        pieces.append(text)
    return pieces

def chunk_text(text, size, overlap):
    paragraphs = re.split(r"\n{2,}", text)
    chunks = []
    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) + 2 > size and current:
            chunks.append(current.strip())
            if overlap > 0 and len(current) > overlap:
                current = current[-overlap:] + "\n\n" + para
            else:
                current = para
        else:
            current = current + "\n\n" + para if current else para
    if current.strip():
        chunks.append(current.strip())
    if not chunks:
        chunks = [text.strip()]
    final = []
    for c in chunks:
        if len(c) > MAX_CHUNK_CHARS:
            final.extend(hard_split(c, MAX_CHUNK_CHARS))
        else:
            final.append(c)
    return final

data_path = pathlib.Path(data_dir)
files = sorted(
    p for p in data_path.rglob("*")
    if p.is_file() and p.suffix.lower() in (".md", ".txt") and p.name != ".gitkeep"
)

print(f"Found {len(files)} files in {data_dir}", flush=True)
if FORCE_REINGEST:
    print("FORCE_REINGEST=1: skipping manifest, reprocessing all files.", flush=True)

manifest = {} if FORCE_REINGEST else load_manifest()

all_ids = []
all_docs = []
all_metas = []
all_valid_ids = set()
new_manifest = {}

skipped_files = 0
reprocessed_files = 0

for fpath in files:
    stat = fpath.stat()
    mtime = stat.st_mtime
    size = stat.st_size
    rel = str(fpath.relative_to(data_path))
    entry = manifest.get(rel)

    if entry and entry.get("mtime") == mtime and entry.get("size") == size:
        cached_ids = entry.get("chunk_ids", [])
        all_valid_ids.update(cached_ids)
        new_manifest[rel] = entry
        skipped_files += 1
        continue

    reprocessed_files += 1
    raw = fpath.read_text(errors="replace")
    title = extract_title(raw) or fpath.stem
    body = strip_frontmatter(raw)
    if not body.strip():
        new_manifest[rel] = {"mtime": mtime, "size": size, "chunk_ids": []}
        continue
    chunks = chunk_text(body, chunk_size, chunk_overlap)
    file_ids = []
    for i, chunk in enumerate(chunks):
        doc_id = hashlib.sha256(f"{rel}::{i}".encode()).hexdigest()[:16]
        file_ids.append(doc_id)
        all_ids.append(doc_id)
        all_docs.append(chunk)
        all_metas.append({"source": rel, "title": title, "chunk_index": i})
    all_valid_ids.update(file_ids)
    new_manifest[rel] = {"mtime": mtime, "size": size, "chunk_ids": file_ids}

print(f"Upserting {len(all_ids)} chunks into '{collection_name}'...", flush=True)

batch = 20
failed = 0
for start in range(0, len(all_ids), batch):
    end = start + batch
    try:
        collection.upsert(
            ids=all_ids[start:end],
            documents=all_docs[start:end],
            metadatas=all_metas[start:end],
        )
    except Exception:
        for j in range(start, min(end, len(all_ids))):
            try:
                collection.upsert(ids=[all_ids[j]], documents=[all_docs[j]], metadatas=[all_metas[j]])
            except Exception as e2:
                failed += 1
                print(f"  SKIP chunk {j} ({all_metas[j]['source']}:{all_metas[j]['chunk_index']}, {len(all_docs[j])} chars): {e2}", flush=True)
    done = min(end, len(all_ids))
    print(f"  {done}/{len(all_ids)}", flush=True)

if failed:
    print(f"WARNING: {failed} chunks skipped due to embedding errors.", flush=True)

existing_result = collection.get(include=[])
existing_ids = set(existing_result["ids"])
orphan_ids = list(existing_ids - all_valid_ids)

orphan_batch_size = 100
for start in range(0, len(orphan_ids), orphan_batch_size):
    collection.delete(ids=orphan_ids[start:start + orphan_batch_size])

if orphan_ids:
    print(f"Deleted {len(orphan_ids)} orphaned chunks.", flush=True)

save_manifest(new_manifest)

total_valid_chunks = len(all_valid_ids)
print(
    f"Done. Collection '{collection_name}' has {collection.count()} chunks. "
    f"[total valid={total_valid_chunks}, skipped files={skipped_files}, "
    f"reprocessed files={reprocessed_files}, orphans deleted={len(orphan_ids)}]",
    flush=True,
)
