
def _build_file_citation_annotations(
    results: List[VectorStoreSearchResult],
    text: str,
) -> List[Dict[str, Any]]:
    """
    Build file_citation annotations for the text.
    Each result with a file_id gets a citation at the end of the text.
    """
    annotations: List[Dict[str, Any]] = []
    index = len(text)  # cite at end of text block
    seen_file_ids: set = set()

    for result in results:
        file_id = _get_field(result, "file_id")
        filename = _get_field(result, "filename")
        if not file_id or file_id in seen_file_ids:
            continue
        seen_file_ids.add(file_id)
        annotations.append(
            {
                "type": "file_citation",
                "index": index,
                "file_id": file_id,
                "filename": filename or "",
            }
        )

    return annotations

