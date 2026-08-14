from chunkers.sentence import chunk_sentence
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def chunk_semantic(
    text: str,
    threshold_type: str = "percentile", # "percentile" or "absolute"
    threshold_value: float = 30.0,      # e.g., 30th percentile or 0.3 absolute similarity
    min_sentences_per_chunk: int = 1
) -> list[dict]:
    """
    Splits text semantically using TF-IDF sentence representation and cosine similarity.
    Returns a list of dicts: {"text": str, "start_index": int, "end_index": int, "sentences": list}
    """
    if not text:
        return []
        
    # Step 1: Split into sentences with positions
    sentences = chunk_sentence(text)
    if len(sentences) <= min_sentences_per_chunk:
        return [{"text": text, "start_index": 0, "end_index": len(text)}]
        
    # Extract sentence texts
    sent_texts = [s["text"] for s in sentences]
    
    # Step 2: Vectorize sentences using TF-IDF
    # We use a combination of word and char n-grams to capture both semantic words and morphology/stem overlaps
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        analyzer="word",
        min_df=1,
        stop_words="english"
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform(sent_texts)
    except Exception:
        # Fallback to no stop words if vocabulary is empty
        try:
            vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
            tfidf_matrix = vectorizer.fit_transform(sent_texts)
        except Exception:
            # If vectorization fails entirely (e.g. all sentences are punctuation), group all
            return [{"text": text, "start_index": 0, "end_index": len(text)}]

    # Step 3: Compute cosine similarities between adjacent sentences
    # Since tfidf_matrix is L2 normalized, cosine similarity is just the dot product
    similarities = []
    for i in range(len(sentences) - 1):
        vec1 = tfidf_matrix[i]
        vec2 = tfidf_matrix[i + 1]
        sim = vec1.dot(vec2.T).toarray()[0][0]
        similarities.append(sim)
        
    if not similarities:
        return [{"text": text, "start_index": 0, "end_index": len(text)}]

    # Step 4: Determine split boundaries
    splits = [] # True if we should split between sentences[i] and sentences[i+1]
    
    if threshold_type == "percentile":
        # threshold_value is a percentile, e.g. 30 (representing the lowest 30% of similarities)
        # We split where similarity is less than this percentile
        cutoff = np.percentile(similarities, threshold_value)
        splits = [sim < cutoff for sim in similarities]
    else:
        # threshold_value is an absolute similarity, e.g. 0.2
        # We split where similarity is less than this absolute value
        splits = [sim < threshold_value for sim in similarities]
        
    # Step 5: Group sentences into chunks based on splits
    chunks = []
    curr_chunk_sents = [sentences[0]]
    
    for i in range(len(similarities)):
        should_split = splits[i]
        next_sentence = sentences[i + 1]
        
        # Enforce min sentences constraint: do not split if current chunk is too small
        if should_split and len(curr_chunk_sents) >= min_sentences_per_chunk:
            # Close current chunk
            s_idx = curr_chunk_sents[0]["start_index"]
            e_idx = curr_chunk_sents[-1]["end_index"]
            chunks.append({
                "text": text[s_idx:e_idx],
                "start_index": s_idx,
                "end_index": e_idx,
                "similarity_to_next": similarities[i] # record similarity at the boundary
            })
            curr_chunk_sents = [next_sentence]
        else:
            curr_chunk_sents.append(next_sentence)
            
    # Add final chunk
    if curr_chunk_sents:
        s_idx = curr_chunk_sents[0]["start_index"]
        e_idx = curr_chunk_sents[-1]["end_index"]
        chunks.append({
            "text": text[s_idx:e_idx],
            "start_index": s_idx,
            "end_index": e_idx,
            "similarity_to_next": 1.0 # default for last chunk
        })
        
    return chunks
