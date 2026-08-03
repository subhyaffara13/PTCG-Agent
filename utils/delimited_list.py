from typing import Union

def delimited_list(
    expr: Union[str, ParserElement],
    delim: Union[str, ParserElement] = ",",
    combine: bool = False,
    min: typing.Optional[int] = None,
    max: typing.Optional[int] = None,
    *,
    allow_trailing_delim: bool = False,
) -> ParserElement:
    """
    .. deprecated:: 3.1.0
       Use the :class:`DelimitedList` class instead.
    """
    return DelimitedList(
        expr, delim, combine, min, max, allow_trailing_delim=allow_trailing_delim
    )


def delimitedList(expr, delim=",", combine=False):
    """Helper to define a delimited list of expressions - the delimiter
    defaults to ','. By default, the list elements and delimiters can
    have intervening whitespace, and comments, but this can be
    overridden by passing ``combine=True`` in the constructor. If
    ``combine`` is set to ``True``, the matching tokens are
    returned as a single token string, with the delimiters included;
    otherwise, the matching tokens are returned as a list of tokens,
    with the delimiters suppressed.

    Example::

        delimitedList(Word(alphas)).parseString("aa,bb,cc") # -> ['aa', 'bb', 'cc']
        delimitedList(Word(hexnums), delim=':', combine=True).parseString("AA:BB:CC:DD:EE") # -> ['AA:BB:CC:DD:EE']
    """
    dlName = _ustr(expr) + " [" + _ustr(delim) + " " + _ustr(expr) + "]..."
    if combine:
        return Combine(expr + ZeroOrMore(delim + expr)).setName(dlName)
    else:
        return (expr + ZeroOrMore(Suppress(delim) + expr)).setName(dlName)

