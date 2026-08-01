
def _osc8_link(text: str, url: str) -> str:
    """Wrap text in an OSC 8 terminal hyperlink."""
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

