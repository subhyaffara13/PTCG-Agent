
def _format_text_block_lines(text: str) -> Iterator[str]:
    for line in text.split("\n"):
        yield f"  {line}"

