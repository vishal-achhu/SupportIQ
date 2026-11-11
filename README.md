# SupportIQ — AI-Powered Customer Support & Knowledge Intelligence

<p align="center">
  <strong>A document-grounded support assistant with an optional LLM response layer</strong><br/>
  Python · FastAPI · Node.js · Express · React · TypeScript · PostgreSQL
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white" />
  <img alt="Node.js" src="https://img.shields.io/badge/Node.js-22-339933?logo=nodedotjs&logoColor=white" />
  <img alt="Express" src="https://img.shields.io/badge/Express-Gateway-000000?logo=express&logoColor=white" />
  <img alt="React" src="https://img.shields.io/badge/React-TypeScript-61DAFB?logo=react&logoColor=black" />
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker_Compose-2496ED?logo=docker&logoColor=white" />
</p>

SupportIQ is a portfolio project for document-based knowledge retrieval and customer support. Users upload PDF, DOCX, TXT, or Markdown files. The Python service extracts text, splits it into overlapping chunks, stores the chunks in PostgreSQL, and retrieves relevant passages with PostgreSQL full-text search. If an LLM API is configured, retrieved passages are sent as context for answer generation. Otherwise, the service can return relevant excerpts as a fallback. A support-ticket workflow is also included.

> **Technical accuracy:** This implementation uses PostgreSQL lexical full-text search. It does **not** currently generate embeddings or perform vector similarity search. The LLM connection is optional. Redis is included in Docker Compose but is not integrated into application logic. The cloud deployment guide is a blueprint, not evidence of a live deployment.

## Contents

- [Overview](#overview)
- [Visual tour](#visual-tour)
- [Architecture](#architecture)
- [Key features](#key-features)
- [How document Q&A works](#how-document-qa-works)
- [Technology stack](#technology-stack)
- [Repository structure](#repository-structure)
- [Run locally](#run-locally)
- [Try the demo](#try-the-demo)
- [API reference](#api-reference)
- [Example question flow](#example-question-flow)
- [Retrieval design and RAG concepts](#retrieval-design-and-rag-concepts)
- [Testing and verification](#testing-and-verification)
- [Security considerations](#security-considerations)
- [Known limitations and roadmap](#known-limitations-and-roadmap)
- [Interview talking points](#interview-talking-points)

## Overview

Support teams often need to search through policy documents, product guides, and internal procedures to answer recurring questions. SupportIQ provides a single workspace to upload knowledge files, ask questions, inspect retrieved source excerpts, and manage support tickets.

### Main user journeys

1. Register or sign in to a workspace.
2. Upload a supported knowledge document.
3. Allow the backend to extract, chunk, and index its text.
4. Ask a question about the uploaded knowledge.
5. Review the response and the source excerpts used by retrieval.
6. Create and track support tickets from the same workspace.

## Visual tour

### Workspace interface preview

![SupportIQ document assistant preview](docs/images/ui-preview.png)

*This is an illustrative documentation preview based on the current React components, not a captured screenshot of a running application. Replace it with a browser screenshot after launching the project and uploading a test document.*

### System architecture

![SupportIQ architecture](docs/images/architecture.svg)

### Document Q&A lifecycle

![SupportIQ RAG workflow](docs/images/rag-workflow.svg)

## Architecture

| Component | Responsibility | Technologies |
|---|---|---|
| Web client | Login, document upload, chat, ticket UI | React, TypeScript, Vite |
| API gateway | Browser-facing API entry point and proxy | Node.js 22, Express, TypeScript |
| AI/application service | Authentication, ingestion, retrieval, LLM orchestration, tickets | Python 3.12, FastAPI |
| Data store | Users, document metadata, text chunks, tickets | PostgreSQL 16 |
| Generation provider | Optional context-based answer generation | OpenAI-compatible chat completions API |
| Runtime | Local service orchestration | Docker Compose |

**Request path:** Browser → Node/Express gateway → Python/FastAPI service → PostgreSQL and, optionally, an LLM provider. The gateway forwards API traffic; the Python service owns the document and AI workflow.

## Key features

### Document ingestion

- Upload PDF, DOCX, TXT, and Markdown files.
- Enforce the configured 10 MB upload limit.
- Extract text using format-specific processing.
- Normalize and split text into overlapping chunks.
- Store document metadata and chunks in PostgreSQL.

### Document question answering

- Accept a natural-language question.
- Search stored chunks using PostgreSQL full-text search.
- Retrieve a limited set of relevant passages.
- Optionally send the question and retrieved context to an LLM API.
- Return the generated answer with source filenames and excerpts.
- Return relevant excerpts when LLM generation is not configured.

### Support tickets

- Create tickets with subject and description.
- List existing tickets.
- Update ticket status.

### Authentication

- Workspace registration and login.
- JWT access token.
- Protected application endpoints.

## How document Q&A works

1. **Upload:** The frontend sends a document through the Express gateway to FastAPI.
2. **Validate:** The service checks the supported extension and configured size limit.
3. **Extract:** Text is extracted from the PDF, DOCX, TXT, or Markdown file.
4. **Chunk:** Long text is divided into smaller overlapping sections.
5. **Persist:** Document metadata and text chunks are stored in PostgreSQL.
6. **Retrieve:** A user's question is converted into a PostgreSQL full-text query. Matching chunks are selected using PostgreSQL text-search functions.
7. **Generate (optional):** The retrieved context and question are sent to the configured LLM chat-completions endpoint.
8. **Return:** The API responds with an answer and source filenames/excerpts. Without LLM configuration, it returns a retrieval-based excerpt response.

## Technology stack

- **Python 3.12 / FastAPI:** document ingestion, retrieval, authentication, ticket endpoints, and LLM orchestration.
- **Pydantic:** typed request/response validation.
- **Node.js 22 / Express / TypeScript:** API gateway between the browser and FastAPI.
- **React / TypeScript / Vite:** interactive workspace UI.
- **PostgreSQL 16:** relational persistence and full-text search.
- **LLM API:** optional answer generation using retrieved context.
- **Docker Compose:** local multi-container development environment.

## Repository structure

```text
SupportIQ/
├── ai-service/             # FastAPI app: ingestion, retrieval, LLM, tickets
├── gateway/                # Node.js + Express API gateway
├── frontend/               # React + TypeScript workspace
├── docs/
│   ├── images/              # README diagrams and illustrative preview
│   ├── architecture.md
│   └── cloud-deployment.md
├── .github/workflows/       # CI starter
├── docker-compose.yml
├── .env.example
└── README.md
```

## Clone and run the project

You can run SupportIQ with Docker Compose (recommended for the first run) or start PostgreSQL, the Python API, Node.js gateway, and React frontend separately. The commands below use Windows PowerShell, with macOS/Linux alternatives where useful.

### Prerequisites

**For either method**

- Git, if cloning from GitHub.
- Internet access to download dependencies.

**Docker method**

- Docker Desktop on Windows/macOS, or Docker Engine + Docker Compose plugin on Linux.
- Docker Desktop must be running before executing Compose commands.

**Manual / no-Docker method**

- Python 3.12 recommended.
- Node.js 22 recommended, with npm.
- PostgreSQL 16 (or a compatible supported PostgreSQL version).

### 1. Clone this repository to your computer

Create the GitHub repository for this project, then copy its HTTPS URL using **Code → HTTPS**. Replace the placeholder below with your actual GitHub username/repository URL:

```bash
git clone https://github.com/<your-github-username>/SupportIQ.git
cd SupportIQ
```

For example, `git clone https://github.com/octocat/SupportIQ.git` is the format of the command; use your own repository URL.

If the project is not on GitHub yet, download the ZIP, extract it, and open a terminal in the extracted `SupportIQ` folder. Confirm that this folder contains `docker-compose.yml`, `.env.example`, and `README.md`.

To download later commits after cloning:

```bash
git pull origin main
```

If your default branch has a different name, replace `main` with that branch name.

### Option A — Run with Docker Compose (recommended)

1. Open a terminal in the repository root (the directory containing `docker-compose.yml`).
2. Create the local environment file:

   **Windows PowerShell**
   ```powershell
   Copy-Item .env.example .env
   ```

   **macOS/Linux**
   ```bash
   cp .env.example .env
   ```

3. Open `.env`. Set a long random `JWT_SECRET`. The LLM integration is optional: leave `LLM_API_KEY` empty to use the retrieval/excerpt fallback, or add a valid compatible provider key to enable generated answers. Keep secrets out of Git.
4. Build and start all services:

   ```bash
   docker compose up --build
   ```

5. Open the application:

   | Service | Local URL |
   |---|---|
   | React frontend | http://localhost:5173 |
   | Node.js/Express gateway | http://localhost:3000 |
   | Gateway health | http://localhost:3000/health |
   | Python FastAPI docs | http://localhost:8000/docs |
   | Python health | http://localhost:8000/health |
   | PostgreSQL | `localhost:5432` |

6. In the frontend, choose **Create your workspace**, register with your name, email, and password, then sign in.
7. Upload a small PDF, DOCX, TXT, or Markdown file (maximum 10 MB), then ask a question answered by that document. Create a ticket to try the ticket workflow.

**Stop the services** with `Ctrl+C`, then run:

```bash
docker compose down
```

To also delete the PostgreSQL volume and all locally stored documents' metadata/chunks, users, and tickets (destructive):

```bash
docker compose down -v
```

### Option B — Run without Docker

This mode requires PostgreSQL to be installed and running locally. Start the database first, then start FastAPI, the Node gateway, and the frontend in separate terminals. The gateway proxies browser API requests to FastAPI.

#### 1. Create the PostgreSQL user and database

Start PostgreSQL. In pgAdmin or `psql`, execute:

```sql
CREATE USER supportiq WITH PASSWORD 'change_me_local';
CREATE DATABASE supportiq OWNER supportiq;
```

If the user already exists, update its password instead of creating it again. Make sure PostgreSQL is listening on port `5432` or adjust the connection URL in the next step.

#### 2. Configure the environment

At the project root, create the example environment file:

**Windows PowerShell**
```powershell
Copy-Item .env.example .env
```

**macOS/Linux**
```bash
cp .env.example .env
```

Processes launched manually do not automatically read `.env`. Set the environment variables in the terminal where each relevant service starts. For the Python service, use a local database hostname (`localhost`), not the Compose service hostname (`postgres`).

#### 3. Start the Python FastAPI service

Open **Terminal 1** at the repository root:

```powershell
cd ai-service
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Set the service variables in this same PowerShell terminal:

```powershell
$env:DATABASE_URL="postgresql+psycopg://supportiq:change_me_local@localhost:5432/supportiq"
$env:JWT_SECRET="replace-with-a-long-random-secret-of-at-least-32-characters"
$env:JWT_EXPIRATION_MINUTES="60"
$env:LLM_BASE_URL="https://api.openai.com/v1"
$env:LLM_API_KEY=""
$env:LLM_MODEL="gpt-4o-mini"
```

Change the database password to match your local PostgreSQL user. To enable LLM generation, set `LLM_API_KEY` to a valid key for the configured compatible provider. Keep the key in the backend environment only; never place it in frontend code.

Start FastAPI:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

On macOS/Linux, activate the virtual environment with `source .venv/bin/activate`. Then open http://localhost:8000/docs and http://localhost:8000/health.

#### 4. Start the Node.js/Express gateway

Open **Terminal 2** at the repository root:

```powershell
cd gateway
npm install
$env:PYTHON_API_URL="http://localhost:8000"
$env:PORT="3000"
npm run dev
```

The gateway health endpoint is http://localhost:3000/health. Its `/api` routes are forwarded to the FastAPI service.

#### 5. Start the React frontend

Open **Terminal 3** at the repository root:

```powershell
cd frontend
npm install
$env:VITE_GATEWAY_URL="http://localhost:3000/api"
npm run dev
```

On macOS/Linux, use `export VITE_GATEWAY_URL=http://localhost:3000/api` before `npm run dev`. Open http://localhost:5173.

#### 6. Test the application

1. Register an account and sign in.
2. Upload a supported document under 10 MB.
3. Ask a question whose answer is present in the document.
4. Review the answer and the source excerpts returned by retrieval.
5. Create a support ticket and update its status.
6. If no LLM API key is configured, verify that the excerpt-based fallback still returns relevant passages.

#### 7. Stop the services

Press `Ctrl+C` in each of the three application terminals. Deactivate the Python virtual environment with `deactivate` if desired. Stop PostgreSQL separately through its service manager or local PostgreSQL application.

### Local ports

| Component | Default port |
|---|---:|
| React/Vite frontend | 5173 |
| Node.js/Express gateway | 3000 |
| Python/FastAPI service | 8000 |
| PostgreSQL | 5432 |
| Redis container (not currently used by application logic) | 6379 |

### Troubleshooting

- **`git` is not recognized:** Install Git, reopen the terminal, and check `git --version`.
- **Docker engine unavailable:** Start Docker Desktop and wait until the engine is ready.
- **Port already allocated:** Stop the conflicting process or change the host port mapping in `docker-compose.yml`.
- **Database connection refused:** Confirm PostgreSQL is running, port `5432` is reachable, and the username/password/database in `DATABASE_URL` are correct.
- **`ModuleNotFoundError`:** Activate the `ai-service` virtual environment and run `pip install -r requirements.txt` there.
- **PowerShell activation is blocked:** Use an approved execution policy or activate the environment from Command Prompt with `.venv\Scripts\activate.bat`.
- **Gateway returns 502:** Confirm FastAPI is running on port `8000` and `PYTHON_API_URL` points to `http://localhost:8000` for manual execution.
- **Frontend API requests fail:** Confirm the gateway is running and `VITE_GATEWAY_URL` is `http://localhost:3000/api`.
- **LLM errors:** Check the provider's API key, model name, base URL, account access, and available quota. Document retrieval can still be demonstrated without the LLM key.

> **Important:** This is a local development/portfolio setup, not a production deployment. The current retrieval implementation uses PostgreSQL full-text search, not embedding-based vector search. Apply production-grade secrets management, file scanning, access controls, monitoring, backups, and deployment hardening before hosting it publicly.

## Try the demo

1. Start SupportIQ and create an account.
2. Upload a small PDF, DOCX, TXT, or Markdown knowledge document (up to 10 MB).
3. Wait for the upload confirmation.
4. Ask a question whose answer is present in the document.
5. Inspect the returned answer and source excerpts.
6. Create a support ticket and refresh the workspace to see it listed.
7. Repeat with the LLM API key omitted to demonstrate the excerpt-based fallback.

### Optional LLM configuration

The application can retrieve document passages without an LLM provider. To enable generated answers, configure the compatible provider values in `.env` using the variable names already present in `.env.example` (including `LLM_API_KEY` and `LLM_MODEL` where applicable), then restart the stack:

```bash
docker compose up --build
```

Keep API keys server-side. Do not put them in frontend code or commit them to Git.

## API reference

Gateway base URL: `http://localhost:3000/api`

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/auth/register` | Register workspace user |
| `POST` | `/auth/login` | Authenticate and obtain JWT |
| `POST` | `/documents/upload` | Upload and process a knowledge document |
| `GET` | `/documents` | List uploaded documents |
| `POST` | `/chat/ask` | Retrieve context and answer a question |
| `GET` | `/tickets` | List support tickets |
| `POST` | `/tickets` | Create a support ticket |
| `PATCH` | `/tickets/{id}` | Update ticket status |

The FastAPI service also exposes interactive OpenAPI documentation at http://localhost:8000/docs.

## Example question flow

A sample knowledge file might contain:

```text
Refund policy: Customers may request a refund within 30 days
of purchase when they provide the original order reference.
```

Example question:

```text
What is the refund request window?
```

Expected retrieval target: the passage containing the 30-day refund window. The exact answer wording and returned excerpt depend on the uploaded document and retrieval result; this README does not claim a measured accuracy score or a fixed model output.

## Retrieval design and RAG concepts

The application demonstrates a basic retrieval-augmented generation workflow, with an important qualification: its retrieval layer is keyword/lexical PostgreSQL full-text search, not vector-based semantic search.

- `to_tsvector` converts document text into a searchable representation.
- `plainto_tsquery` converts a plain-language query into a text-search query.
- Matching chunks are selected and passed to the optional generation step.
- The LLM prompt is instructed to use supplied context and disclose when evidence is insufficient.

### Current implementation vs. future semantic retrieval

| Capability | Current project | Possible enhancement |
|---|---|---|
| Text extraction | Implemented for supported formats | OCR for scanned PDFs/images |
| Chunking | Overlapping text chunks | Token-aware chunking |
| Retrieval | PostgreSQL full-text search | Embeddings + pgvector/vector store |
| Ranking | Lexical search matching | Hybrid search + reranking |
| Generation | Optional LLM API | Model evaluation and provider abstraction |
| Sources | Filenames and excerpts | Page/section-level citations |

## Testing and verification

A document-ingestion test and a GitHub Actions CI starter are included. Before describing the project as fully verified, run the app in your own environment and test registration, login, upload, retrieval, LLM fallback, and ticket operations.

Suggested test command from `ai-service` in a Python environment:

```bash
pytest
```

Also verify the full Docker Compose startup and the gateway-to-FastAPI request path. This README does not claim a successful runtime test or benchmark result.

## Security considerations

Uploaded documents and their contents must be treated as untrusted input. Before production use:

- Enforce ownership/tenant isolation on every document, chunk, and ticket query.
- Verify actual file signatures and MIME types, not only extensions.
- Add malware scanning, quotas, and safer object storage.
- Add rate limiting, refresh-token rotation, password reset, and MFA.
- Keep provider API keys in a server-side secret manager.
- Add prompt-injection defenses and make retrieved content an untrusted context boundary.
- Add logging, monitoring, retention rules, and audit trails.

## Known limitations and roadmap

- [ ] Add embedding generation and vector retrieval (for example, pgvector).
- [ ] Add hybrid keyword + semantic retrieval and reranking.
- [ ] Build a curated evaluation set for retrieval relevance and answer faithfulness.
- [ ] Improve source citations with page and section metadata.
- [ ] Complete tenant isolation and document-level access control.
- [ ] Add malware scanning and stronger upload validation.
- [ ] Add prompt-injection tests and safeguards.
- [ ] Integrate Redis only when a concrete caching/queue use case is defined (currently infrastructure only).
- [ ] Deploy to a cloud environment; current deployment notes are a blueprint only.



## License

See [`LICENSE`](LICENSE).
