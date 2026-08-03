import json

def _toolset_from_row(row) -> MCPToolset:
    data = row.model_dump()
    tools = data.get("tools") or []
    if isinstance(tools, str):
        tools = json.loads(tools)
    data["tools"] = tools
    return MCPToolset(**data)

