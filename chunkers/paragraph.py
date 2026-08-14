import re

def chunk_paragraph(text: str) -> list[dict]:
    """
    Splits text by double newlines (paragraphs).
    Returns a list of dicts: {"text": str, "start_index": int, "end_index": int}
    """
    if not text:
        return []
        
    # Split by double newlines (possibly with whitespace inside)
    paragraph_split = re.compile(r'\n\s*\n')
    raw_paras = paragraph_split.split(text)
    
    chunks = []
    last_search_idx = 0
    
    for para in raw_paras:
        if not para.strip():
            continue
            
        # Find exact character indices in original text
        start_char = text.find(para, last_search_idx)
        if start_char == -1:
            start_char = text.find(para)
            
        if start_char == -1:
            start_char = last_search_idx
            end_char = min(len(text), start_char + len(para))
        else:
            end_char = start_char + len(para)
            
        chunks.append({
            "text": para,
            "start_index": start_char,
            "end_index": end_char
        })
        last_search_idx = end_char
        
    return chunks
