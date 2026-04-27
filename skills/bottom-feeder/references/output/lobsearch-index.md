# lobsearch-index

After writing knowledge files:
1. If knowledge-search ingest is available, trigger/refresh index.
2. If ingest is not available, log "index pending" in daily note.
3. Record file paths produced so later jobs can re-index.

Never block the run on indexing failures.
