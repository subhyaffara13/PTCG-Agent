
def _sanitize_help_text(text: str) -> str:
    """Sanitizes the help text by removing rich tags"""
    if not importlib.util.find_spec("rich"):
        return text
    from . import rich_utils

    return rich_utils.rich_render_text(text)

