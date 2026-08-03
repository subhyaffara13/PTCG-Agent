from typing import Dict

def _handle_content_block_start(data: Dict, content_blocks: Dict[int, Dict]) -> None:
    idx = data.get("index", len(content_blocks))
    block = data.get("content_block", {})
    block_type = block.get("type", "text")

    _BLOCK_TEMPLATES: Dict[str, Dict] = {
        "text": {"type": "text", "text": ""},
        "thinking": {"type": "thinking", "thinking": "", "signature": ""},
        "redacted_thinking": {
            "type": "redacted_thinking",
            "data": block.get("data", ""),
        },
    }
    if block_type == "tool_use":
        content_blocks[idx] = {
            "type": "tool_use",
            "id": block.get("id", ""),
            "name": block.get("name", ""),
            "input": {},
            "_partial_json": "",
        }
    elif block_type in _BLOCK_TEMPLATES:
        content_blocks[idx] = dict(_BLOCK_TEMPLATES[block_type])
    else:
        content_blocks[idx] = dict(block)

