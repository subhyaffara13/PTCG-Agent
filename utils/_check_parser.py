
def _check_parser(parser: str) -> None:
    """
    Make sure a valid parser is passed.

    Parameters
    ----------
    parser : str

    Raises
    ------
    KeyError
      * If an invalid parser is passed
    """
    if parser not in PARSERS:
        raise KeyError(
            f"Invalid parser '{parser}' passed, valid parsers are {PARSERS.keys()}"
        )

