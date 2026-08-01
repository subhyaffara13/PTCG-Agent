
def normalize_text(
    text: str, line_len: int = DEFAULT_LINE_LENGTH, indent: str = ""
) -> str:
    """Wrap the text on the given line length."""
    return "\n".join(
        textwrap.wrap(
            text, width=line_len, initial_indent=indent, subsequent_indent=indent
        )
    )

