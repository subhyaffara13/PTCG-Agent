from typing import Any, List

def _has_gemini_search_tool(tools: List[Any]) -> bool:
    from litellm.llms.vertex_ai.gemini.vertex_and_google_ai_studio_gemini import (
        VertexGeminiConfig,
    )

    search_tool_keys = VertexGeminiConfig._search_tool_keys()
    return any(
        isinstance(tool, dict) and any(key in tool for key in search_tool_keys)
        for tool in tools
    )

