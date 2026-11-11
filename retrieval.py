from sqlalchemy import text
from sqlalchemy.orm import Session

def retrieve(db: Session, owner_id: int, question: str, top_k: int = 5):
    # PostgreSQL full-text search; a later vector-search milestone can use pgvector.
    sql = text('''
      SELECT dc.content, d.filename, ts_rank(to_tsvector('english', dc.content),
             plainto_tsquery('english', :question)) AS score
      FROM document_chunks dc
      JOIN documents d ON d.id = dc.document_id
      WHERE dc.owner_id = :owner_id
        AND to_tsvector('english', dc.content) @@ plainto_tsquery('english', :question)
      ORDER BY score DESC
      LIMIT :top_k
    ''')
    return db.execute(sql, {"owner_id": owner_id, "question": question, "top_k": top_k}).mappings().all()
