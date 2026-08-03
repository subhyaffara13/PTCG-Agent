from typing import Any

def replace_with(repl_str: Any) -> ParseAction:
    """
    Helper method for common parse actions that simply return
    a literal value.  Especially useful when used with
    :meth:`~ParserElement.transform_string`.

    Example:

    .. doctest::

       >>> num = Word(nums).set_parse_action(lambda toks: int(toks[0]))
       >>> na = one_of("N/A NA").set_parse_action(replace_with(math.nan))
       >>> term = na | num

       >>> term[1, ...].parse_string("324 234 N/A 234")
       ParseResults([324, 234, nan, 234], {})
    """
    return lambda s, l, t: [repl_str]


def replaceWith(replStr):
    """Helper method for common parse actions that simply return
    a literal value.  Especially useful when used with
    :class:`transformString<ParserElement.transformString>` ().

    Example::

        num = Word(nums).setParseAction(lambda toks: int(toks[0]))
        na = oneOf("N/A NA").setParseAction(replaceWith(math.nan))
        term = na | num

        OneOrMore(term).parseString("324 234 N/A 234") # -> [324, 234, nan, 234]
    """
    return lambda s, l, t: [replStr]

