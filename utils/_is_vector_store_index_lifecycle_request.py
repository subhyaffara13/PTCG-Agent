
def _is_vector_store_index_lifecycle_request(
    request_method: str,
    request_path: str,
    index_name: str,
) -> bool:
    """
    True when the request creates or deletes a search index itself (not documents).

    Examples (admin-only):
    - DELETE /azure_ai/indexes/my-index
    - PUT /azure_ai/indexes/my-index
    - POST /azure_ai/indexes
    """
    if request_method not in ("POST", "PUT", "DELETE", "PATCH"):
        return False

    suffix = _suffix_after_index_name(request_path, index_name)
    if suffix is not None:
        # Document operations live under /indexes/{name}/docs/...
        if suffix.startswith("/docs"):
            return False
        # DELETE/PUT/PATCH on /indexes/{name} itself is index lifecycle.
        if suffix == "" or suffix.startswith("?"):
            return True

    # POST /indexes (create index at service level; no index name in path).
    normalized = request_path.rstrip("/")
    if request_method == "POST" and normalized.endswith("/indexes"):
        return True

    return False

