from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select
from .db import Base, engine, get_db
from .models import User, Document, DocumentChunk, Ticket
from .schemas import RegisterIn, LoginIn, TicketIn, TicketStatusIn, AskIn
from .security import hash_password, verify_password, make_token
from .dependencies import get_current_user
from .ingestion import extract_text, chunk_text
from .retrieval import retrieve
from .llm import answer_with_llm

app = FastAPI(title="SupportIQ AI Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173","http://localhost:3000"], allow_methods=["*"], allow_headers=["*"])
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status":"UP","service":"supportiq-ai"}

@app.post("/auth/register", status_code=201)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    email = payload.email.lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(409, "Email already registered")
    user = User(name=payload.name, email=email, password_hash=hash_password(payload.password))
    db.add(user); db.commit(); db.refresh(user)
    return {"message":"Account created"}

@app.post("/auth/login")
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    return {"accessToken":make_token(user),"tokenType":"Bearer"}

@app.post("/documents/upload", status_code=201)
async def upload_document(file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    name = file.filename or "uploaded-file"
    if len(name) > 255:
        raise HTTPException(400, "Filename too long")
    data = await file.read()
    if len(data) > 10 * 1024 * 1024:
        raise HTTPException(413, "Maximum upload size is 10 MB")
    try:
        text_content = extract_text(name, data)
    except ValueError as exc:
        raise HTTPException(415, str(exc))
    if not text_content.strip():
        raise HTTPException(400, "No extractable text found")
    doc = Document(filename=name, content_type=file.content_type or "application/octet-stream", owner_id=user.id)
    db.add(doc); db.flush()
    chunks = chunk_text(text_content)
    for index, content in enumerate(chunks):
        db.add(DocumentChunk(document_id=doc.id, chunk_index=index, content=content, owner_id=user.id))
    db.commit()
    return {"id":doc.id,"filename":name,"chunksCreated":len(chunks)}

@app.get("/documents")
def list_documents(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    docs = db.scalars(select(Document).where(Document.owner_id == user.id).order_by(Document.id.desc())).all()
    return [{"id":d.id,"filename":d.filename,"createdAt":d.created_at.isoformat() if d.created_at else None} for d in docs]

@app.post("/chat/ask")
async def ask(payload: AskIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = retrieve(db, user.id, payload.question, payload.top_k)
    passages = [{"filename":r["filename"],"content":r["content"]} for r in rows]
    answer = await answer_with_llm(payload.question, passages)
    sources = [{"filename":p["filename"],"excerpt":p["content"][:280]} for p in passages]
    return {"answer":answer,"sources":sources,"retrieval":"postgres-full-text-search"}

@app.get("/tickets")
def list_tickets(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.scalars(select(Ticket).where(Ticket.owner_id == user.id).order_by(Ticket.id.desc())).all()
    return [{"id":t.id,"subject":t.subject,"description":t.description,"status":t.status,"priority":t.priority} for t in rows]

@app.post("/tickets", status_code=201)
def create_ticket(payload: TicketIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    priority = payload.priority.upper()
    if priority not in {"LOW","NORMAL","HIGH","URGENT"}:
        raise HTTPException(400,"Invalid priority")
    ticket = Ticket(subject=payload.subject,description=payload.description,priority=priority,owner_id=user.id)
    db.add(ticket);db.commit();db.refresh(ticket)
    return {"id":ticket.id,"subject":ticket.subject,"status":ticket.status,"priority":ticket.priority}

@app.patch("/tickets/{ticket_id}")
def update_ticket(ticket_id:int, payload:TicketStatusIn, user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    ticket = db.scalar(select(Ticket).where(Ticket.id==ticket_id,Ticket.owner_id==user.id))
    if not ticket: raise HTTPException(404,"Ticket not found")
    status = payload.status.upper()
    if status not in {"OPEN","IN_PROGRESS","RESOLVED","CLOSED"}: raise HTTPException(400,"Invalid status")
    ticket.status=status;db.commit()
    return {"id":ticket.id,"status":ticket.status}
