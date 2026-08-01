
def _build_search_results_for_include(
    results: List[VectorStoreSearchResult],
) -> List[Dict[str, Any]]:
    """
    Convert VectorStoreSearchResult objects to the format expected in
    file_search_call.search_results (mirrors OpenAI's include= format).

    All chunks are returned — no deduplication by file_id — matching the
    behaviour of OpenAI's native file_search which surfaces every relevant
    chunk even when multiple chunks originate from the same document.
    """
    formatted: List[Dict[str, Any]] = []
    for result in results:
        file_id = _get_field(result, "file_id") or ""
        content_items = _get_field(result, "content") or []
        text_chunks = [
            c.get("text", "") if isinstance(c, dict) else getattr(c, "text", "")
            for c in content_items
        ]
        text = " ".join(t for t in text_chunks if t)
        formatted.append(
            {
                "file_id": file_id,
                "filename": _get_field(result, "filename") or "",
                "score": _get_field(result, "score"),
                "text": text,
                "attributes": _get_field(result, "attributes") or {},
            }
        )
    return formatted

