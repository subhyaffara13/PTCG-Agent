from typing import List

def _format_search_results_as_tool_output(
    results: List[VectorStoreSearchResult],
) -> str:
    """Serialize search results into a string to pass back as the tool's output."""
    if not results:
        return "No results found in the vector store."

    parts: List[str] = []
    for i, result in enumerate(results, 1):
        score = _get_field(result, "score")
        file_id = _get_field(result, "file_id")
        filename = _get_field(result, "filename")
        content_items = _get_field(result, "content") or []
        text_chunks = [
            c.get("text", "") if isinstance(c, dict) else getattr(c, "text", "")
            for c in content_items
        ]
        text = " ".join(t for t in text_chunks if t)

        header = f"[Result {i}"
        if filename:
            header += f" | {filename}"
        if file_id:
            header += f" | file_id={file_id}"
        if score is not None:
            header += f" | score={score:.3f}"
        header += "]"

        parts.append(f"{header}\n{text}")

    return "\n\n".join(parts)

