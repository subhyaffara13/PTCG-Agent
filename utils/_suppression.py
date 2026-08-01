
def _suppression(expr: Union[ParserElement, str]) -> ParserElement:
    # internal helper to avoid wrapping Suppress inside another Suppress
    if isinstance(expr, Suppress):
        return expr
    return Suppress(expr)

