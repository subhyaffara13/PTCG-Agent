from typing import List

def _extract_mcp_tool_names(data: dict) -> List[str]:
    """MCP call_tool: name or mcp_tool_name in body"""
    names: List[str] = []
    name = data.get("name") or data.get("mcp_tool_name")
    if name:
        names.append(str(name))
    return names

