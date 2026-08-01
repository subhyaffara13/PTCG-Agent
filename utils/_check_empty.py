
def _check_empty(data: utils.Buffer) -> None:
    """All data should have been parsed."""
    if data:
        raise ValueError("Corrupt data: unparsed data")

