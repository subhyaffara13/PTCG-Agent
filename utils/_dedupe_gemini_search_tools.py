
def _dedupe_gemini_search_tools(tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    from litellm.llms.vertex_ai.gemini.vertex_and_google_ai_studio_gemini import (
        VertexGeminiConfig,
    )

    search_tool_keys = VertexGeminiConfig._search_tool_keys()
    seen_search_keys: set[str] = set()
    deduped_tools: List[Dict[str, Any]] = []

    for tool in tools:
        if not isinstance(tool, dict):
            deduped_tools.append(tool)
            continue

        search_key = next((key for key in search_tool_keys if key in tool), None)
        if search_key is None:
            deduped_tools.append(tool)
            continue

        if search_key in seen_search_keys:
            continue

        seen_search_keys.add(search_key)
        deduped_tools.append(tool)

    return deduped_tools

