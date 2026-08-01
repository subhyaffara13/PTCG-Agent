
def _replace_file_search_tools(
    tools: Optional[Iterable[ToolParam]],
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Replace all file_search tools with a single function tool.

    Returns:
        (new_tools_list, all_vector_store_ids)
    """
    non_file_search: List[Dict[str, Any]] = []
    vector_store_ids: List[str] = []

    for tool in tools or []:
        if isinstance(tool, dict) and tool.get("type") == "file_search":
            ids = tool.get("vector_store_ids") or []
            vector_store_ids.extend(ids)
        else:
            non_file_search.append(tool)

    # Deduplicate while preserving order
    unique_ids: List[str] = list(dict.fromkeys(vector_store_ids))
    if unique_ids:
        non_file_search.append(_build_function_tool(unique_ids))

    return non_file_search, unique_ids

