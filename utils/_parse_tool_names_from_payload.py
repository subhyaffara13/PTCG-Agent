from typing import Any, Dict, Set

def _parse_tool_names_from_payload(payload: Dict[str, Any]) -> Set[str]:
    """
    Extract deduplicated tool names from a spend log payload.
    Sources: mcp_namespaced_tool_name, response (tool_calls), proxy_server_request (tools).
    """
    tool_names: Set[str] = set()

    # Top-level MCP tool name (single tool per request for that flow)
    mcp_name = payload.get("mcp_namespaced_tool_name")
    if mcp_name and isinstance(mcp_name, str) and mcp_name.strip():
        tool_names.add(mcp_name.strip())

    # Response: OpenAI-style tool_calls[].function.name or choices[0].message.tool_calls
    response_raw = payload.get("response")
    if response_raw:
        response_obj = (
            safe_json_loads(response_raw, default=None)
            if isinstance(response_raw, str)
            else response_raw
        )
        if isinstance(response_obj, dict):
            _add_tool_calls_to_set(response_obj.get("tool_calls"), tool_names)
            choices = response_obj.get("choices")
            if isinstance(choices, list) and choices:
                msg = (
                    choices[0].get("message") if isinstance(choices[0], dict) else None
                )
                if isinstance(msg, dict):
                    _add_tool_calls_to_set(msg.get("tool_calls"), tool_names)

    # Request body: tools[].function.name
    request_raw = payload.get("proxy_server_request")
    if request_raw:
        request_obj = (
            safe_json_loads(request_raw, default=None)
            if isinstance(request_raw, str)
            else request_raw
        )
        if isinstance(request_obj, dict):
            body = request_obj.get("body", request_obj)
            if isinstance(body, dict):
                request_obj = body
        if isinstance(request_obj, dict):
            tools = request_obj.get("tools")
            if isinstance(tools, list):
                for t in tools:
                    if isinstance(t, dict):
                        fn = t.get("function")
                        if isinstance(fn, dict):
                            name = fn.get("name")
                            if name and isinstance(name, str) and name.strip():
                                tool_names.add(name.strip())

    return tool_names

