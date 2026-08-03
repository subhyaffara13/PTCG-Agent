from typing import Any, Dict

def _handle_generic_metadata(
    path: str, op_type: str, value: Any, metadata: Dict[str, Any]
) -> None:
    """Handle generic metadata operations for unknown paths."""
    if op_type == "remove":
        metadata.pop(path, None)
    else:
        metadata[path] = value

