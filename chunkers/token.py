import tiktoken

def chunk_token(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
    encoding_name: str = "cl100k_base"
) -> list[dict]:
    """
    Splits text based on the number of tokens using tiktoken.
    Returns a list of dicts: {"text": str, "start_index": int, "end_index": int, "token_count": int}
    """
    if not text:
        return []
        
    try:
        encoding = tiktoken.get_encoding(encoding_name)
    except Exception:
        # Fallback to default encoding
        encoding = tiktoken.get_encoding("cl100k_base")
        
    tokens = encoding.encode(text)
    token_len = len(tokens)
    
    if chunk_size <= 0:
        return [{"text": text, "start_index": 0, "end_index": len(text), "token_count": token_len}]
        
    # Bound overlap
    if chunk_overlap >= chunk_size:
        chunk_overlap = chunk_size - 1
    if chunk_overlap < 0:
        chunk_overlap = 0
        
    step = chunk_size - chunk_overlap
    chunks = []
    
    start_tok = 0
    last_search_idx = 0
    
    while start_tok < token_len:
        end_tok = min(start_tok + chunk_size, token_len)
        chunk_tokens = tokens[start_tok:end_tok]
        chunk_text = encoding.decode(chunk_tokens)
        
        # Find exact character indices in original text
        # Search starting from last_search_idx to handle duplicate strings
        start_char = text.find(chunk_text, last_search_idx)
        if start_char == -1:
            # Fallback if find fails (e.g., weird token decoding differences)
            start_char = text.find(chunk_text)
            
        if start_char == -1:
            # Fallback to character approximation
            start_char = last_search_idx
            end_char = min(len(text), start_char + len(chunk_text))
        else:
            end_char = start_char + len(chunk_text)
            
        chunks.append({
            "text": chunk_text,
            "start_index": start_char,
            "end_index": end_char,
            "token_count": len(chunk_tokens)
        })
        
        # Advance search index to the start of this chunk plus one character
        last_search_idx = start_char + 1
        
        if end_tok >= token_len:
            break
            
        start_tok += step
        
    return chunks
