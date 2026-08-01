
def escape_html(text, table=_escape_html_table):
    """Escape &, <, > as well as single and double quotes for HTML."""
    return text.translate(table)


def escape_html(text):
    """Escape &, <, > as well as single and double quotes for HTML."""
    return text.replace('&', '&amp;').  \
                replace('<', '&lt;').   \
                replace('>', '&gt;').   \
                replace('"', '&quot;'). \
                replace("'", '&#39;')


def escapeHtml(raw: str) -> str:
    """Replace special characters "&", "<", ">" and '"' to HTML-safe sequences."""
    # like html.escape, but without escaping single quotes
    raw = raw.replace("&", "&amp;")  # Must be done first!
    raw = raw.replace("<", "&lt;")
    raw = raw.replace(">", "&gt;")
    raw = raw.replace('"', "&quot;")
    return raw

