# chunk_data.py
import re, os, json, unicodedata
 
INPUT_DIR  = '/Users/gourabsaha/Downloads/Project_AT101/atguru-platform/data/extracted_text'
OUTPUT_DIR = '/Users/gourabsaha/Downloads/Project_AT101/atguru-platform/data/chunks'
os.makedirs(OUTPUT_DIR, exist_ok=True)
 
CHUNK_SIZE = 400   # words per chunk
OVERLAP    = 50    # words overlap between chunks
 
def clean_text(text):
    # Normalise Bengali Unicode (important for consistency)
    text = unicodedata.normalize('NFC', text)
    # Remove non-Bengali characters except common punctuation
    text = re.sub(r'[^\u0980-\u09FF\s।,;:!?()"\'-]', ' ', text)
    # Collapse multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text
 
def chunk_text(text, book_name, book_number):
    words = text.split()
    chunks = []
    idx = 0
    start = 0
    while start < len(words):
        end = start + CHUNK_SIZE
        chunk_words = words[start:end]
        chunk_text  = ' '.join(chunk_words)
        if len(chunk_words) > 50:  # skip very short chunks
            chunks.append({
                'id':          f'book{book_number:03d}_chunk{idx:04d}',
                'text':        chunk_text,
                'book_name':   book_name,
                'book_number': book_number,
                'chunk_index': idx,
            })
            idx += 1
        start += CHUNK_SIZE - OVERLAP
    return chunks
 
all_chunks = []
for i, filename in enumerate(sorted(os.listdir(INPUT_DIR))):
    if filename.endswith('.txt'):
        book_name = filename.replace('.txt', '')
        with open(os.path.join(INPUT_DIR, filename), encoding='utf-8') as f:
            raw = f.read()
        cleaned = clean_text(raw)
        chunks  = chunk_text(cleaned, book_name, i + 1)
        all_chunks.extend(chunks)
        print(f'{book_name}: {len(chunks)} chunks')
 
# Save to JSON
out_path = os.path.join(OUTPUT_DIR, 'all_chunks.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)
 
print(f'Total chunks: {len(all_chunks)}')
