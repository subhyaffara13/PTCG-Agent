
def ungroup(expr: ParserElement) -> ParserElement:
    """Helper to undo pyparsing's default grouping of And expressions,
    even if all but one are non-empty.
    """
    return TokenConverter(expr).add_parse_action(lambda t: t[0])


def ungroup(expr):
    """Helper to undo pyparsing's default grouping of And expressions,
    even if all but one are non-empty.
    """
    return TokenConverter(expr).addParseAction(lambda t: t[0])

