#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: bash query.sh \"<question>\" [n_results]"
    exit 1
fi

QUERY="$1"
N_RESULTS="${2:-3}"

CHROMA_PERSIST_DIR="${CHROMA_PERSIST_DIR:-$HOME/.openclaw/chroma/knowledge-search}"
CHROMA_COLLECTION="${CHROMA_COLLECTION:-knowledge}"
OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"
EMBEDDING_MODEL="${EMBEDDING_MODEL:-nomic-embed-text}"

python3 - "$QUERY" "$N_RESULTS" "$CHROMA_PERSIST_DIR" "$CHROMA_COLLECTION" "$OLLAMA_URL" "$EMBEDDING_MODEL" <<'PYEOF'
import sys, json

query = sys.argv[1]
n_results = int(sys.argv[2])
persist_dir = sys.argv[3]
collection_name = sys.argv[4]
ollama_url = sys.argv[5]
model_name = sys.argv[6]

import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from chromadb.errors import NotFoundError

ef = OllamaEmbeddingFunction(model_name=model_name, url=ollama_url)
client = chromadb.PersistentClient(path=persist_dir)

try:
    collection = client.get_collection(name=collection_name, embedding_function=ef)
except NotFoundError:
    print(json.dumps({
        "error": f"Collection '{collection_name}' does not exist yet.",
        "hint": "Run ingest.sh first to index documents before querying."
    }, indent=2))
    sys.exit(0)

results = collection.query(query_texts=[query], n_results=n_results, include=["documents", "metadatas", "distances"])

output = []
for i in range(len(results["ids"][0])):
    meta = results["metadatas"][0][i]
    dist = results["distances"][0][i]
    doc = results["documents"][0][i]
    output.append({
        "rank": i + 1,
        "title": meta.get("title", ""),
        "source": meta.get("source", ""),
        "distance": round(dist, 4),
        "excerpt": doc[:500] + ("..." if len(doc) > 500 else ""),
    })

print(json.dumps(output, indent=2))
PYEOF
