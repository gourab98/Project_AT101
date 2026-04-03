import os

# Path to your folder
folder_path = "/Users/gourabsaha/Downloads/Project_AT101/atguru-platform/data/raw_pdfs"

# Get all PDF files
files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

# Sort files (important for consistent numbering)
files.sort()

# Rename files
for i, filename in enumerate(files, start=1):
    new_name = f"book_{i:03}.pdf"
    
    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_name)
    
    os.rename(old_path, new_path)

print("Renaming completed!")