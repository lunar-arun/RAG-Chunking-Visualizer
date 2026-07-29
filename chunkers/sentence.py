import re
import nltk

# Global flag to track NLTK availability
_nltk_initialized = False

def initialize_nltk():
    global _nltk_initialized
    if _nltk_initialized:
        return True
    try:
        # Try downloading 'punkt' silently
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True) # for newer NLTK versions
        _nltk_initialized = True
        return True
    except Exception:
        # Fallback if download fails
        return False

def regex_split_sentences(text: str) -> list[str]:
    """
    Fallback sentence splitter using regex.
    Splits text by . or ! or ? followed by whitespace and a capital letter or number.
    """
    if not text:
        return []
    # Split at period, exclamation mark, or question mark followed by whitespace
    sentence_end = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"\'])')
    raw_sentences = sentence_end.split(text)
    return [s for s in raw_sentences if s.strip()]

def chunk_sentence(text: str) -> list[dict]:
    """
    Splits text into sentences.
    Returns a list of dicts: {"text": str, "start_index": int, "end_index": int}
    """
    if not text:
        return []
        
    sentences = []
    
    # Try NLTK first
    nltk_success = initialize_nltk()
    if nltk_success:
        try:
            sentences = nltk.tokenize.sent_tokenize(text)
        except Exception:
            sentences = regex_split_sentences(text)
    else:
        sentences = regex_split_sentences(text)
        
    chunks = []
    last_search_idx = 0
    
    for sent in sentences:
        if not sent.strip():
            continue
            
        start_char = text.find(sent, last_search_idx)
        if start_char == -1:
            start_char = text.find(sent)
            
        if start_char == -1:
            # Fallback
            start_char = last_search_idx
            end_char = min(len(text), start_char + len(sent))
        else:
            end_char = start_char + len(sent)
            
        chunks.append({
            "text": sent,
            "start_index": start_char,
            "end_index": end_char
        })
        last_search_idx = end_char
        
    return chunks
