
def _build_file_search_call_output(
    call_id: str,
    queries: List[str],
    results: Optional[List[VectorStoreSearchResult]] = None,
    include_search_results: bool = False,
) -> Dict[str, Any]:
    """Build the file_search_call output item (mirrors OpenAI's format).

    Args:
        call_id: Unique ID for this file_search call.
        queries: List of search queries used.
        results: The raw search results (used when include_search_results=True).
        include_search_results: Populate search_results when the caller passed
            ``include=["file_search_call.results"]``.
    """
    search_results = None
    if include_search_results and results:
        search_results = _build_search_results_for_include(results)
    return {
        "type": "file_search_call",
        "id": call_id,
        "status": "completed",
        "queries": queries,
        "search_results": search_results,
    }

