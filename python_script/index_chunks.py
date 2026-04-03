# index_chunks.py
import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
 
COLLECTION = 'guru_scriptures'
CHUNKS_FILE = '/Users/gourabsaha/Downloads/Project_AT101/atguru-platform/data/chunks/all_chunks.json'
 
# Load chunks
with open(CHUNKS_FILE, encoding='utf-8') as f:
    chunks = json.load(f)
 
print(f'Loaded {len(chunks)} chunks')
 
# Load LaBSE model (Bengali-aware, free, runs locally)
print('Loading LaBSE embedding model...')
model = SentenceTransformer('sentence-transformers/LaBSE')
 
# Generate embeddings in batches
print('Generating embeddings...')
texts = [c['text'] for c in chunks]
embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)

# Connect to Qdrant
client = QdrantClient('localhost', port=6333)
 
# Create collection (delete first if it already exists)
if client.collection_exists(COLLECTION):
    client.delete_collection(COLLECTION)
 
client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)
 
# Upload all points
print('Uploading to Qdrant...')
points = [
    PointStruct(
        id=i,
        vector=embeddings[i].tolist(),
        payload=chunks[i]   # store metadata alongside vector
    )
    for i in range(len(chunks))
]
 
# Upload in batches of 500
batch_size = 500
for i in range(0, len(points), batch_size):
    batch = points[i:i+batch_size]
    client.upsert(collection_name=COLLECTION, points=batch)
    print(f'  Uploaded {min(i+batch_size, len(points))}/{len(points)}')
 
print('Indexing complete!')
