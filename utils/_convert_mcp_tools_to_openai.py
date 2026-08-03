from typing import Any, Dict, List, Optional

def _convert_mcp_tools_to_openai(
    tools: Optional[List["Tool"]],
) -> Optional[List[Dict[str, Any]]]:
    """
    Convert MCP Tool definitions to OpenAI function calling format.
    MCP Tool: {name, description, inputSchema}
    OpenAI Tool: {type: "function", function: {name, description, parameters}}
    """
    if not tools:
        return None
    openai_tools = []
    for tool in tools:
        openai_tool = {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.inputSchema
                or {
                    "type": "object",
                    "properties": {},
                },
            },
        }
        openai_tools.append(openai_tool)
    return openai_tools

