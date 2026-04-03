# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import ollama
 
app = FastAPI(title='Guru Scripture API')
 
# Allow the React frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# Load embedding model once at startup
embed_model  = SentenceTransformer('sentence-transformers/LaBSE')
qdrant_client = QdrantClient('localhost', port=6333)
COLLECTION   = 'guru_scriptures'
 
SYSTEM_PROMPT = """
You are a spiritual guide answering questions based solely on the
teachings and writings of the guru. You must:
1. Answer ONLY using the provided scripture passages.
2. If the answer is not in the passages, say so honestly.
3. Speak with humility and in the spirit of the guru's teachings.
4. If the question is in Bengali, answer in Bengali.
5. Never fabricate or add information beyond the passages.
"""

class Query(BaseModel):
    question: str
    top_k: int = 5   # number of passages to retrieve
 
@app.post('/ask')
async def ask(query: Query):
    if not query.question.strip():
        raise HTTPException(status_code=400, detail='Question cannot be empty')
 
    # Step 1: Embed the question
    q_vector = embed_model.encode(query.question).tolist()
 
    # Step 2: Search Qdrant for relevant passages
    results = qdrant_client.query_points(
    collection_name=COLLECTION,
    query=q_vector,
    limit=query.top_k,
    with_payload=True
    ).points
 
    if not results:
        return {'answer': 'No relevant passages found.', 'sources': []}
# Step 3: Build context from retrieved chunks
    context_parts = []
    for r in results:
        p = r.payload
        context_parts.append(
            f"[Source: {p['book_name']}, Chunk {p['chunk_index']}]\n{p['text']}"
        )
    context = '\n\n---\n\n'.join(context_parts)
 
    # Step 4: Call local Ollama LLM
    user_message = f'Scripture Passages:\n{context}\n\nQuestion: {query.question}'
    response = ollama.chat(
        model='llama3.1',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user',   'content': user_message},
        ]
    )
 
    answer  = response['message']['content']
    sources = list(set(r.payload['book_name'] for r in results))
 
    return {'answer': answer, 'sources': sources}
 
@app.get('/health')
def health():
    return {'status': 'ok'}
