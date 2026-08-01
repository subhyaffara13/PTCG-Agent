
def _collect_response_file_search_vector_store_ids(data: Dict[str, Any]) -> set[str]:
    vector_store_ids: set[str] = set()
    tools = data.get("tools")
    if not isinstance(tools, list):
        return vector_store_ids

    for tool in tools:
        if not isinstance(tool, dict) or tool.get("type") != "file_search":
            continue
        ids = tool.get("vector_store_ids") or []
        if not isinstance(ids, list):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "file_search.vector_store_ids must be a list of strings"
                },
            )
        for vector_store_id in ids:
            if not isinstance(vector_store_id, str) or not vector_store_id:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "file_search.vector_store_ids must be a list of strings"
                    },
                )
            vector_store_ids.add(vector_store_id)

    return vector_store_ids

