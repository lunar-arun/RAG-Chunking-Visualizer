def chunk_character(text: str, chunk_size: int, chunk_overlap: int) -> list[dict]:
    """
    Splits text into chunks of exact character size with a specified character overlap.
    Returns a list of dicts: {"text": str, "start_index": int, "end_index": int}
    """
    if not text:
        return []
    
    text_len = len(text)
    if chunk_size <= 0:
        return [{"text": text, "start_index": 0, "end_index": text_len}]
    
    # Bound overlap size
    if chunk_overlap >= chunk_size:
        chunk_overlap = chunk_size - 1
    if chunk_overlap < 0:
        chunk_overlap = 0
        
    step = chunk_size - chunk_overlap
    chunks = []
    
    start = 0
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk_text = text[start:end]
        chunks.append({
            "text": chunk_text,
            "start_index": start,
            "end_index": end
        })
        if end >= text_len:
            break
        start += step
        
    return chunks
