import tiktoken

def chunk_sliding_window(
    text: str,
    window_size: int,
    step_size: int,
    use_tokens: bool = False,
    encoding_name: str = "cl100k_base"
) -> list[dict]:
    """
    Slices the text using a sliding window.
    Supports either character-based or token-based sliding.
    Returns a list of dicts: {"text": str, "start_index": int, "end_index": int}
    """
    if not text:
        return []
        
    if window_size <= 0:
        return [{"text": text, "start_index": 0, "end_index": len(text)}]
        
    if step_size <= 0:
        step_size = window_size
        
    chunks = []
    
    if not use_tokens:
        # Character-based sliding window
        text_len = len(text)
        start = 0
        while start < text_len:
            end = min(start + window_size, text_len)
            chunks.append({
                "text": text[start:end],
                "start_index": start,
                "end_index": end
            })
            if end >= text_len:
                break
            start += step_size
    else:
        # Token-based sliding window
        try:
            encoding = tiktoken.get_encoding(encoding_name)
        except Exception:
            encoding = tiktoken.get_encoding("cl100k_base")
            
        tokens = encoding.encode(text)
        token_len = len(tokens)
        
        start_tok = 0
        last_search_idx = 0
        
        while start_tok < token_len:
            end_tok = min(start_tok + window_size, token_len)
            chunk_tokens = tokens[start_tok:end_tok]
            chunk_text = encoding.decode(chunk_tokens)
            
            # Find index in original text
            start_char = text.find(chunk_text, last_search_idx)
            if start_char == -1:
                start_char = text.find(chunk_text)
                
            if start_char == -1:
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
            
            last_search_idx = start_char + 1
            
            if end_tok >= token_len:
                break
                
            start_tok += step_size
            
    return chunks
