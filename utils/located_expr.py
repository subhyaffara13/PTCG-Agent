
def locatedExpr(expr: ParserElement) -> ParserElement:
    """
    .. deprecated:: 3.0.0
       Use the :class:`Located` class instead. Note that `Located`
       returns results with one less grouping level.

    Helper to decorate a returned token with its starting and ending
    locations in the input string.

    This helper adds the following results names:

    - ``locn_start`` - location where matched expression begins
    - ``locn_end`` - location where matched expression ends
    - ``value`` - the actual parsed results

    Be careful if the input text contains ``<TAB>`` characters, you
    may want to call :meth:`ParserElement.parse_with_tabs`
    """
    warnings.warn(
        f"{'locatedExpr'!r} deprecated - use {'Located'!r}",
        PyparsingDeprecationWarning,
        stacklevel=2,
    )

    locator = Empty().set_parse_action(lambda ss, ll, tt: ll)
    return Group(
        locator("locn_start")
        + expr("value")
        + locator.copy().leave_whitespace()("locn_end")
    )


def locatedExpr(expr):
    """Helper to decorate a returned token with its starting and ending
    locations in the input string.

    This helper adds the following results names:

     - locn_start = location where matched expression begins
     - locn_end = location where matched expression ends
     - value = the actual parsed results

    Be careful if the input text contains ``<TAB>`` characters, you
    may want to call :class:`ParserElement.parseWithTabs`

    Example::

        wd = Word(alphas)
        for match in locatedExpr(wd).searchString("ljsdf123lksdjjf123lkkjj1222"):
            print(match)

    prints::

        [[0, 'ljsdf', 5]]
        [[8, 'lksdjjf', 15]]
        [[18, 'lkkjj', 23]]
    """
    locator = Empty().setParseAction(lambda s, l, t: l)
    return Group(locator("locn_start") + expr("value") + locator.copy().leaveWhitespace()("locn_end"))

