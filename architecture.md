# Architecture and interview notes

## Why separate Node and Python?
- Node/Express acts as the browser-facing API gateway and gives a clear JavaScript/TypeScript backend story.
- FastAPI owns document ingestion, retrieval, and LLM orchestration, keeping AI dependencies in the Python service.
- PostgreSQL stores users, document metadata, chunks, and tickets.
- The React client calls one gateway origin.

## RAG lifecycle
1. Ingest: validate file type and size, extract text, normalize whitespace.
2. Chunk: split text into overlapping windows.
3. Index: store chunks with document and owner metadata.
4. Retrieve: use PostgreSQL `to_tsvector` and `plainto_tsquery` to rank matching passages.
5. Generate: optionally call an OpenAI-compatible chat completions endpoint with retrieved passages.
6. Ground: prompt the model to use only supplied context and disclose insufficient evidence.
7. Attribute: return source filenames and excerpts.

## Important limitation
This starter implements lexical full-text retrieval, not embedding-based semantic search. Add embeddings + pgvector (or another vector store), hybrid retrieval, reranking, and a benchmark set before claiming advanced production RAG.

## Security work to complete
- Enforce tenant isolation on every query and file operation.
- Verify file signatures, scan uploads, and use object storage.
- Add refresh tokens, MFA, rate limits, and audit logs.
- Treat uploaded document content as untrusted and defend against prompt injection.
- Keep API keys in a secret manager; never send them to the browser.
