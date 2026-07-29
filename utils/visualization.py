import html
import streamlit as st

def get_hsl_color(idx: int, alpha: float = 0.15) -> str:
    """
    Generates a pleasing HSL background color based on the golden ratio,
    optimized for Light Mode.
    """
    hue = (idx * 137.5) % 360
    # Soft pastel background for light mode
    return f"hsla({hue:.1f}, 80%, 75%, {alpha:.2f})"

def get_hsl_border(idx: int, alpha: float = 0.5) -> str:
    """
    Generates a matching border color for the HSL background,
    optimized for Light Mode.
    """
    hue = (idx * 137.5) % 360
    return f"hsla({hue:.1f}, 80%, 55%, {alpha:.2f})"



def get_chunk_overlap_intervals(chunks: list[dict], k: int) -> list[tuple[int, int]]:
    """
    Finds the character index intervals in chunk k that overlap with chunk k-1 or chunk k+1.
    Returns intervals as list of tuples (start, end) relative to chunk k's local text.
    """
    if k < 0 or k >= len(chunks):
        return []
        
    chunk = chunks[k]
    S = chunk["start_index"]
    E = chunk["end_index"]
    chunk_len = E - S
    
    if chunk_len <= 0:
        return []
        
    overlap_ranges = []
    
    # Check overlap with previous chunk (k - 1)
    if k > 0:
        E_prev = chunks[k - 1]["end_index"]
        if S < E_prev:
            overlap_end_local = min(chunk_len, E_prev - S)
            if overlap_end_local > 0:
                overlap_ranges.append((0, overlap_end_local))
                
    # Check overlap with next chunk (k + 1)
    if k < len(chunks) - 1:
        S_next = chunks[k + 1]["start_index"]
        if S_next < E:
            overlap_start_local = max(0, S_next - S)
            if overlap_start_local < chunk_len:
                overlap_ranges.append((overlap_start_local, chunk_len))
                
    # Merge overlapping local ranges
    # Since there are at most 2 ranges (one at start, one at end), merging is simple:
    if len(overlap_ranges) == 2:
        r1, r2 = overlap_ranges
        # If they overlap, merge them into a single range
        if r1[1] >= r2[0]:
            return [(r1[0], max(r1[1], r2[1]))]
            
    return overlap_ranges

def format_chunk_text_with_bold_overlaps(chunks: list[dict], k: int, is_html: bool = True) -> str:
    """
    Formats the text of chunk k, wrapping overlapping parts in bold tags (HTML <b> or Markdown **).
    """
    chunk = chunks[k]
    chunk_text = chunk["text"]
    
    overlap_intervals = get_chunk_overlap_intervals(chunks, k)
    if not overlap_intervals:
        return html.escape(chunk_text) if is_html else chunk_text
        
    # Get all boundary points
    endpoints = [0, len(chunk_text)]
    for start, end in overlap_intervals:
        endpoints.extend([start, end])
    endpoints = sorted(list(set(endpoints)))
    
    formatted_parts = []
    
    for i in range(len(endpoints) - 1):
        s = endpoints[i]
        e = endpoints[i + 1]
        part = chunk_text[s:e]
        
        # Check if this sub-segment falls in any overlap interval
        is_overlap = any(start <= s and e <= end for start, end in overlap_intervals)
        
        # Escape HTML if rendering HTML
        part_disp = html.escape(part) if is_html else part
        
        if is_overlap:
            if is_html:
                formatted_parts.append(f'<span class="overlap-bold" style="font-weight: 800;">{part_disp}</span>')
            else:
                formatted_parts.append(f"**{part_disp}**")
        else:
            formatted_parts.append(part_disp)
            
    return "".join(formatted_parts)

def build_inline_visualization_html(original_text: str, chunks: list[dict]) -> str:
    """
    Builds the complete inline visualization of the document, showing alternating colors per chunk,
    and bold styling for overlapping regions, mimicking ChunkViz.
    """
    if not chunks:
        return html.escape(original_text)
        
    # Find all start/end boundaries of all chunks
    boundaries = [0, len(original_text)]
    for c in chunks:
        boundaries.extend([c["start_index"], c["end_index"]])
    boundaries = sorted(list(set(boundaries)))
    
    html_spans = []
    
    for i in range(len(boundaries) - 1):
        s = boundaries[i]
        e = boundaries[i + 1]
        span_text = original_text[s:e]
        if not span_text:
            continue
            
        # Find which chunks cover this interval
        covering_chunks = []
        for idx, c in enumerate(chunks):
            if c["start_index"] <= s and e <= c["end_index"]:
                covering_chunks.append(idx)
                
        escaped_text = html.escape(span_text).replace("\n", "<br>")
        
        if not covering_chunks:
            # Not covered by any chunk
            html_spans.append(f'<span>{escaped_text}</span>')
        elif len(covering_chunks) == 1:
            # Covered by exactly one chunk
            c_idx = covering_chunks[0]
            bg = get_hsl_color(c_idx, alpha=0.2)
            border = get_hsl_border(c_idx, alpha=0.6)
            tooltip = f"Chunk {c_idx + 1}"
            html_spans.append(
                f'<span style="background-color: {bg}; border-bottom: 2px solid {border}; '
                f'padding: 1px 0px; border-radius: 1px; transition: all 0.2s;" '
                f'title="{tooltip}">{escaped_text}</span>'
            )
        else:
            # Overlap! Covered by multiple chunks
            # Render with background of the first covering chunk, but with bold styling and border
            c_idx = covering_chunks[0]
            bg = get_hsl_color(c_idx, alpha=0.3)
            border = get_hsl_border(c_idx, alpha=0.8)
            tooltip = "Overlap: " + ", ".join([f"Chunk {idx + 1}" for idx in covering_chunks])
            html_spans.append(
                f'<span style="background-color: {bg}; border-bottom: 2px dashed {border}; '
                f'font-weight: 800; padding: 1px 0px; border-radius: 1px; transition: all 0.2s;" '
                f'title="{tooltip}">{escaped_text}</span>'
            )
            
    # Wrap in a beautiful container with modern font styling
    css_style = """
    <style>
    .inline-vis-container {
        font-family: 'Outfit', 'Inter', -apple-system, sans-serif;
        line-height: 1.8;
        font-size: 1.05rem;
        color: var(--text-color);
        background-color: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.1);
        max-height: 500px;
        overflow-y: auto;
        white-space: pre-wrap;
    }
    .overlap-bold {
        text-shadow: 0 0 0.5px currentColor;
    }
    </style>
    """
    
    return f'{css_style}<div class="inline-vis-container">{"".join(html_spans)}</div>'
