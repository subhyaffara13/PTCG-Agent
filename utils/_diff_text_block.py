
def _diff_text_block(left: str, right: str) -> Iterator[str]:
    yield "Left:"
    yield from _format_text_block_lines(left)
    yield ""
    yield "Right:"
    yield from _format_text_block_lines(right)

