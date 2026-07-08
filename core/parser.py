import os
from typing import List, Dict

def parse_source_file(file_path: str) -> str:
    """
    Reads a local file, strips out excessive whitespace/empty lines to save tokens,
    and returns its clean content wrapped in structural boundaries.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
        
    filename = os.path.basename(file_path)
    cleaned_lines = []
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            stripped = line.strip()
            # Skip purely empty lines to drastically reduce token usage
            if stripped:
                cleaned_lines.append(line.rstrip())
                
    content = "\n".join(cleaned_lines)
    
    # Wrap the file in a clean, machine-readable format
    return f"--- FILE: {filename} ---\n{content}\n--- END OF FILE ---"