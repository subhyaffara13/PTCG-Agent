
def _collect_block_text(block: dict, holders: List[_StringHolder]) -> None:
    text = block.get("text")
    if isinstance(text, str) and text:
        holders.append((block, "text"))

