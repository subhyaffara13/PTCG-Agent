
def _visible_exprs(exprs: Iterable[pyparsing.ParserElement]):
    non_diagramming_exprs = (
        pyparsing.ParseElementEnhance,
        pyparsing.PositionToken,
        pyparsing.And._ErrorStop,
    )
    return [
        e
        for e in exprs
        if not isinstance(e, non_diagramming_exprs)
    ]

