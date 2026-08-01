
def _handle_content_block_stop(data: Dict, content_blocks: Dict[int, Dict]) -> None:
    idx = data.get("index", 0)
    block = content_blocks.get(idx)
    if block and block.get("type") == "tool_use":
        partial = block.pop("_partial_json", "")
        if partial:
            try:
                block["input"] = json.loads(partial)
            except (json.JSONDecodeError, ValueError):
                block["input"] = {"_raw": partial}

