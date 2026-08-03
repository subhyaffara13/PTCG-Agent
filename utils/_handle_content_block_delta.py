from typing import Dict

def _handle_content_block_delta(data: Dict, content_blocks: Dict[int, Dict]) -> None:
    idx = data.get("index", 0)
    delta = data.get("delta", {})
    delta_type = delta.get("type", "")
    block = content_blocks.get(idx)
    if block is None:
        return

    if delta_type == "text_delta":
        block["text"] = block.get("text", "") + delta.get("text", "")
    elif delta_type == "input_json_delta":
        block["_partial_json"] = block.get("_partial_json", "") + delta.get(
            "partial_json", ""
        )
    elif delta_type == "thinking_delta":
        block["thinking"] = block.get("thinking", "") + delta.get("thinking", "")
    elif delta_type == "signature_delta":
        block["signature"] = delta.get("signature", block.get("signature", ""))

