
def _should_vertical(
    specification: int, exprs: Iterable[pyparsing.ParserElement]
) -> bool:
    """
    Returns true if we should return a vertical list of elements
    """
    if specification is None:
        return False
    else:
        return len(_visible_exprs(exprs)) >= specification

