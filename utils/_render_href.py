import re

def _render_href(x, format):
    """uses regex to detect a common URL pattern and converts to href tag in format."""
    if isinstance(x, str):
        if format == "html":
            href = '<a href="{0}" target="_blank">{0}</a>'
        elif format == "latex":
            href = r"\href{{{0}}}{{{0}}}"
        else:
            raise ValueError("``hyperlinks`` format can only be 'html' or 'latex'")
        pat = r"((http|ftp)s?:\/\/|www.)[\w/\-?=%.:@]+\.[\w/\-&?=%.,':;~!@#$*()\[\]]+"
        return re.sub(pat, lambda m: href.format(m.group(0)), x)
    return x

