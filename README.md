# SupportIQ — AI Customer Support & Knowledge Intelligence

A portfolio-grade GenAI + full-stack application for document-grounded customer support.

## Product capabilities
- Workspace registration and JWT login.
- Upload PDF, DOCX, TXT, and Markdown knowledge files.
- Extract text, split it into overlapping chunks, and store chunk metadata.
- Retrieve relevant passages using PostgreSQL full-text search.
- Generate grounded answers with an optional OpenAI-compatible LLM endpoint.
- Return source file names and excerpts with answers.
- Create and track support tickets.
- Agent dashboard with ticket status and conversation history.
- Node.js/Express API gateway in front of the Python service.
- React + TypeScript frontend.
- PostgreSQL persistence, Redis infrastructure, Docker Compose, and CI starter.

## Technology stack
- Python 3.12, FastAPI, Pydantic
- Node.js 22, Express, TypeScript
- React, TypeScript, Vite
- PostgreSQL 16, SQL, PostgreSQL full-text search
- Redis 7 (infrastructure included; cache integration is an extension point)
- OpenAI-compatible chat completions API (optional)
- Docker, Docker Compose, GitHub Actions

## Architecture

```text
React + TypeScript (5173)
        |
        v
Node.js + Express Gateway (3000)
        |
        v
Python FastAPI AI Service (8000)
        |
        +------ PostgreSQL (5432)
        |
        +------ Optional LLM provider
        |
        +------ Redis (6379, extension point)
```

The Node gateway provides a single browser-facing API boundary and forwards requests to FastAPI. The Python service owns document processing, retrieval, answer generation, and ticket data.

## Run locally

Requirements: Docker Desktop / Docker Engine and Docker Compose.

```bash
cp .env.example .env
docker compose up --build
```

Open:
- Frontend: http://localhost:5173
- Node gateway: http://localhost:3000
- Python API docs: http://localhost:8000/docs

Register an account from the login screen. The LLM integration is optional; without an API key, the service returns a clearly labelled extractive answer based on retrieved passages.

## Environment variables

See `.env.example`. Do not commit real credentials. Configure `LLM_API_KEY` only in your local environment or secret manager.

## API overview (gateway base URL: http://localhost:3000/api)

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/register` | Register workspace user |
| POST | `/auth/login` | Login and obtain token |
| POST | `/documents/upload` | Upload a knowledge document |
| GET | `/documents` | List uploaded documents |
| POST | `/chat/ask` | Retrieve context and answer |
| GET | `/tickets` | List support tickets |
| POST | `/tickets` | Create support ticket |
| PATCH | `/tickets/{id}` | Update ticket status |

## Retrieval and GenAI design
1. Extract plain text from supported document formats.
2. Split text into chunks with overlap to preserve context.
3. Store chunks in PostgreSQL.
4. Use PostgreSQL full-text search to rank candidate passages.
5. Send the selected context and question to the configured LLM.
6. Instruct the model to answer only from context and state when evidence is insufficient.
7. Return answer, source names, and source excerpts.

This first implementation uses PostgreSQL full-text search, not embedding-based semantic retrieval. A natural next milestone is adding embeddings and pgvector or a dedicated vector database, then evaluating retrieval quality on a curated question set.

## Cloud deployment path
A deployment blueprint is included in `docs/cloud-deployment.md`. It describes container hosting, managed PostgreSQL, secrets, HTTPS, logs, and monitoring. The project is not already deployed to a cloud account.

## Before claiming production readiness
- [ ] Add tenant/workspace isolation to every database query.
- [ ] Add file size limits, MIME verification, malware scanning, and storage quotas.
- [ ] Add refresh token rotation, password reset, MFA, and rate limiting.
- [ ] Add embeddings + pgvector and retrieval evaluation.
- [ ] Add prompt-injection defenses and document trust boundaries.
- [ ] Add tests for authentication, upload, retrieval, and ticket workflows.
- [ ] Add observability, structured logs, tracing, and alerting.
- [ ] Add durable object storage for documents.
- [ ] Add retention and deletion policies.
- [ ] Deploy and verify before publishing a live URL.

## Resume-ready description (only after running and verifying)
**SupportIQ — AI-Powered Customer Support & Knowledge Intelligence Platform**  
Developed a full-stack knowledge assistant using Python, FastAPI, Node.js, React, TypeScript, and PostgreSQL. Implemented document ingestion for PDF/DOCX/TXT/Markdown, text extraction and chunking, PostgreSQL full-text retrieval, optional LLM-based grounded responses with source excerpts, and support-ticket workflows. Containerized the services using Docker Compose.
