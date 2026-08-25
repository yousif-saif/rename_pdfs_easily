import os
from pathlib import Path

def get_pdfs():
    base_dir = Path(__file__).resolve().parent / "pdfs"
    if not base_dir.exists():
        return []
    
    pdfs = []
    # Using rglob to recursively find all .pdf files
    for pdf_file in base_dir.rglob("*.pdf"):
        if os.path.isdir(pdf_file):
            continue
        # Get path relative to the base 'pdfs' folder
        rel_path = pdf_file.relative_to(base_dir)
        # Store it as a string with forward slashes for URLs
        pdfs.append(str(rel_path).replace("\\", "/"))
        
    return pdfs
