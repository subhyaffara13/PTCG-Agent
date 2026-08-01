
def comment(string: str) -> Comment:
    """Create a comment item.

    A multiline string produces one ``#``-prefixed line per line so that the
    result is still valid TOML.
    """
    lines = string.split("\n")
    rendered = "\n".join(f"# {line}" if line else "#" for line in lines)
    return Comment(Trivia(comment_ws="  ", comment=rendered))

