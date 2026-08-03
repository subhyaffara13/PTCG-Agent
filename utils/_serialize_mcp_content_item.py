from typing import Any, Dict

def _serialize_mcp_content_item(item: object) -> Dict[str, Any]:
    """Serialize an MCP content item to a JSON-friendly dict.

    Handles raw dicts, MCP SDK Pydantic models, and simple ``.text`` objects.
    """
    if isinstance(item, dict):
        return dict(item)
    model_dump = getattr(item, "model_dump", None)
    if callable(model_dump):
        try:
            return dict(model_dump(exclude_none=True))
        except TypeError:
            return dict(model_dump())
    text = getattr(item, "text", None)
    if isinstance(text, str):
        return {"type": getattr(item, "type", "text"), "text": text}
    return {"type": "text", "text": str(item)}

