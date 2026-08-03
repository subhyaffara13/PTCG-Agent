from typing import List

def extract_request_tool_names(route: str, data: dict) -> List[str]:
    """
    Extract tool names from the request body for the given route.
    Uses guardrail translation handlers when available, else standalone extractors
    for generate_content and MCP. Returns [] for non-tool-capable routes or when
    no tools are present.
    """
    call_types = get_call_types_for_route(route)
    if not call_types:
        return []
    _register_standalone_extractors()
    mappings = load_guardrail_translation_mappings()
    for call_type in call_types:
        if not isinstance(call_type, CallTypes):
            continue
        if call_type.value not in TOOL_CAPABLE_CALL_TYPES:
            continue
        if call_type.value in STANDALONE_EXTRACTORS:
            return STANDALONE_EXTRACTORS[call_type.value](data)
        handler_cls = mappings.get(call_type)
        if handler_cls is not None:
            names = handler_cls().extract_request_tool_names(data)
            if names:
                return names
    return []

