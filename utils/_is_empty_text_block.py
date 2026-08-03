from typing import Any

def _is_empty_text_block(block: Any) -> bool:
    if not isinstance(block, dict) or block.get("type") != "text":
        return False
    text = block.get("text")
    return not isinstance(text, str) or not text.strip()

