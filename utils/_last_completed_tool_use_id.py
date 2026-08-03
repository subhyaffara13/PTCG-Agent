from typing import Any, Dict, List, Optional

def _last_completed_tool_use_id(
    messages: List[Dict[str, Any]],
) -> Optional[str]:
    """Latest completed tool_result id; never cleared."""
    last_id: Optional[str] = None
    for msg in messages:
        content = msg.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    block_id = block.get("tool_use_id")
                    if isinstance(block_id, str):
                        last_id = block_id
    return last_id

