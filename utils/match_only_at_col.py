
def match_only_at_col(n: int) -> ParseAction:
    """
    Helper method for defining parse actions that require matching at
    a specific column in the input text.
    """

    def verify_col(strg: str, locn: int, toks: ParseResults) -> None:
        if col(locn, strg) != n:
            raise ParseException(strg, locn, f"matched token not at column {n}")

    return verify_col


def matchOnlyAtCol(n):
    """Helper method for defining parse actions that require matching at
    a specific column in the input text.
    """
    def verifyCol(strg, locn, toks):
        if col(locn, strg) != n:
            raise ParseException(strg, locn, "matched token not at column %d" % n)
    return verifyCol

