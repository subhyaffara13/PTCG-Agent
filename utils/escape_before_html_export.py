
def escape_before_html_export(input_text: str) -> str:
    """Ensure that the input string can be used for HTML export."""
    return escape(input_text).strip()

