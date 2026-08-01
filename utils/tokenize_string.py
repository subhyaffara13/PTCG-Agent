
def tokenize_string(source: str) -> Iterator[tuple[int, str]]:
    """
    Tokenize a Python source code string.

    Parameters
    ----------
    source : str
        The Python source code string.

    Returns
    -------
    tok_generator : Iterator[Tuple[int, str]]
        An iterator yielding all tokens with only toknum and tokval (Tuple[ing, str]).
    """
    # GH 59285
    # Escape characters, including backticks
    source = "".join(
        (
            create_valid_python_identifier(substring[1:-1])
            if is_backtick_quoted
            else substring
        )
        for is_backtick_quoted, substring in _split_by_backtick(source)
    )

    line_reader = StringIO(source).readline
    token_generator = tokenize.generate_tokens(line_reader)

    for toknum, tokval, _, _, _ in token_generator:
        yield toknum, tokval

