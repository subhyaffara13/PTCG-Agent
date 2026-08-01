
def dummy_highlighter(source: str, lexer: Literal["diff", "python"] = "python") -> str:
    """Dummy highlighter that returns the text unprocessed.

    Needed for _notin_text, as the diff gets post-processed to only show the "+" part.
    """
    return source

