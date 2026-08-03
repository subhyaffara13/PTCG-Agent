from typing import Any, Dict

def map_gemini_image_tools_params(
    non_default_params: Dict[str, Any],
    mapped_params: Dict[str, Any],
) -> Dict[str, Any]:
    from litellm.llms.vertex_ai.gemini.vertex_and_google_ai_studio_gemini import (
        VertexGeminiConfig,
    )

    gemini_config = VertexGeminiConfig()
    result = dict(mapped_params)
    result.pop("web_search_options", None)

    tools_value = non_default_params.get("tools")
    if isinstance(tools_value, list) and tools_value:
        mapped_tools = gemini_config._map_function(
            value=tools_value, optional_params=result
        )
        result = gemini_config._add_tools_to_optional_params(result, mapped_tools)

    web_search_options = non_default_params.get("web_search_options")
    existing_tools = result.get("tools")
    if isinstance(web_search_options, dict) and not (
        isinstance(existing_tools, list) and _has_gemini_search_tool(existing_tools)
    ):
        search_tool = gemini_config._map_web_search_options(web_search_options)
        result = gemini_config._add_tools_to_optional_params(result, [search_tool])

    gemini_config._drop_search_tools_mixed_with_functions(result)

    if isinstance(result.get("tools"), list):
        result["tools"] = _dedupe_gemini_search_tools(result["tools"])

    return result

