
def rich_render_text(text: str) -> str:
    """Remove rich tags and render a pure text representation"""
    console = _get_rich_console()
    return "".join(segment.text for segment in console.render(text)).rstrip("\n")

