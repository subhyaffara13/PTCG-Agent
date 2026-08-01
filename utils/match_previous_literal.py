
def match_previous_literal(expr: ParserElement) -> ParserElement:
    """Helper to define an expression that is indirectly defined from
    the tokens matched in a previous expression, that is, it looks for
    a 'repeat' of a previous expression.  For example::

    .. testcode::

       first = Word(nums)
       second = match_previous_literal(first)
       match_expr = first + ":" + second

    will match ``"1:1"``, but not ``"1:2"``.  Because this
    matches a previous literal, will also match the leading
    ``"1:1"`` in ``"1:10"``. If this is not desired, use
    :class:`match_previous_expr`. Do *not* use with packrat parsing
    enabled.
    """
    rep = Forward()

    def copy_token_to_repeater(s, l, t):
        if not t:
            rep << Empty()
            return

        if len(t) == 1:
            rep << t[0]
            return

        # flatten t tokens
        tflat = _flatten(t.as_list())
        rep << And(Literal(tt) for tt in tflat)

    expr.add_parse_action(copy_token_to_repeater, call_during_try=True)
    rep.set_name(f"(prev) {expr}")
    return rep


def matchPreviousLiteral(expr):
    """Helper to define an expression that is indirectly defined from
    the tokens matched in a previous expression, that is, it looks for
    a 'repeat' of a previous expression.  For example::

        first = Word(nums)
        second = matchPreviousLiteral(first)
        matchExpr = first + ":" + second

    will match ``"1:1"``, but not ``"1:2"``.  Because this
    matches a previous literal, will also match the leading
    ``"1:1"`` in ``"1:10"``. If this is not desired, use
    :class:`matchPreviousExpr`. Do *not* use with packrat parsing
    enabled.
    """
    rep = Forward()
    def copyTokenToRepeater(s, l, t):
        if t:
            if len(t) == 1:
                rep << t[0]
            else:
                # flatten t tokens
                tflat = _flatten(t.asList())
                rep << And(Literal(tt) for tt in tflat)
        else:
            rep << Empty()
    expr.addParseAction(copyTokenToRepeater, callDuringTry=True)
    rep.setName('(prev) ' + _ustr(expr))
    return rep

