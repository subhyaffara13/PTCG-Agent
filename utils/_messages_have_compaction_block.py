from typing import Dict, List

def _messages_have_compaction_block(messages: List[Dict]) -> bool:
    """Return True when any message carries a ``compaction`` content block."""
    for msg in messages:
        content = msg.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "compaction":
                return True
    return False

