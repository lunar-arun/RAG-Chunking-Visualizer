def chunk_recursive(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
    separators: list[str] = None
) -> list[dict]:
    """
    Splits text recursively using a list of separators, then merges them
    to stay within chunk_size while maintaining chunk_overlap.
    Returns a list of dicts: {"text": str, "start_index": int, "end_index": int}
    """
    if not text:
        return []
    
    if separators is None:
        separators = ["\n\n", "\n", " ", ""]
        
    text_len = len(text)
    if chunk_size <= 0:
        return [{"text": text, "start_index": 0, "end_index": text_len}]
        
    # Bound overlap
    if chunk_overlap >= chunk_size:
        chunk_overlap = chunk_size - 1
    if chunk_overlap < 0:
        chunk_overlap = 0

    # Step 1: Recursively split the text into leaf splits (each <= chunk_size or unsplittable)
    def get_splits(txt: str, offset: int, seps: list[str]) -> list[dict]:
        if len(txt) <= chunk_size or not seps:
            # If the block is small enough, or we ran out of separators, return it as a single split
            return [{"text": txt, "start_index": offset, "end_index": offset + len(txt)}]
            
        current_sep = seps[0]
        next_seps = seps[1:]
        
        # If current separator is empty string, we split by characters
        if current_sep == "":
            parts = []
            for i in range(0, len(txt), chunk_size):
                sub = txt[i : i + chunk_size]
                parts.append({"text": sub, "start_index": offset + i, "end_index": offset + i + len(sub)})
            return parts

        # Otherwise, split by the separator
        parts = []
        last_idx = 0
        idx = txt.find(current_sep)
        
        if idx == -1:
            # Separator not found, try the next one on the entire text block
            return get_splits(txt, offset, next_seps)
            
        while idx != -1:
            part_text = txt[last_idx:idx]
            if part_text:
                parts.extend(get_splits(part_text, offset + last_idx, next_seps))
            
            # Record the separator itself as a split or let it be absorbed?
            # Typically separators are absorbed into the preceding split or are just skipped.
            # To keep positions exact, we can include separator text or simply skip it.
            # Let's keep separator text in the split or include it in the offset.
            # We skip separator characters here, but we will adjust start/end indices.
            last_idx = idx + len(current_sep)
            idx = txt.find(current_sep, last_idx)
            
        # Add the remaining text
        remaining = txt[last_idx:]
        if remaining:
            parts.extend(get_splits(remaining, offset + last_idx, next_seps))
            
        return parts

    splits = get_splits(text, 0, separators)
    # Filter out empty splits
    splits = [s for s in splits if len(s["text"]) > 0]
    
    if not splits:
        return []
        
    # Step 2: Merge splits into chunks
    chunks = []
    i = 0
    num_splits = len(splits)
    
    while i < num_splits:
        # Start a new chunk
        chunk_start_split = i
        chunk_end_split = i
        
        # Expand chunk as much as possible within chunk_size
        while chunk_end_split < num_splits:
            # Merged range would be from start of chunk_start_split to end of chunk_end_split
            curr_start = splits[chunk_start_split]["start_index"]
            curr_end = splits[chunk_end_split]["end_index"]
            
            if curr_end - curr_start <= chunk_size:
                chunk_end_split += 1
            else:
                # If even a single split is larger than chunk_size, we must include it
                if chunk_end_split == chunk_start_split:
                    chunk_end_split += 1
                break
                
        # Finalize this chunk
        chunk_end_split = min(chunk_end_split, num_splits)
        s_idx = splits[chunk_start_split]["start_index"]
        e_idx = splits[chunk_end_split - 1]["end_index"]
        
        chunks.append({
            "text": text[s_idx:e_idx],
            "start_index": s_idx,
            "end_index": e_idx
        })
        
        if chunk_end_split == num_splits:
            break
            
        # Backtrack to find the next starting split to satisfy overlap
        # We want splits[next_start]["start_index"] to be as far back as possible, 
        # but splits[chunk_end_split - 1]["end_index"] - splits[next_start]["start_index"] <= chunk_overlap
        next_start = chunk_end_split
        # Search backward from chunk_end_split - 1
        for j in range(chunk_end_split - 1, chunk_start_split, -1):
            overlap_len = splits[chunk_end_split - 1]["end_index"] - splits[j]["start_index"]
            if overlap_len <= chunk_overlap:
                next_start = j
            else:
                break
                
        # If no split was backtracked (e.g. overlap is 0 or splits are too large), move forward
        if next_start == chunk_end_split:
            i = chunk_end_split
        else:
            i = next_start
            
    return chunks
