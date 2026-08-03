from typing import Optional, Union

def infix_notation(
    base_expr: ParserElement,
    op_list: list[InfixNotationOperatorSpec],
    lpar: Union[str, ParserElement] = Suppress("("),
    rpar: Union[str, ParserElement] = Suppress(")"),
) -> Forward:
    """Helper method for constructing grammars of expressions made up of
    operators working in a precedence hierarchy.  Operators may be unary
    or binary, left- or right-associative.  Parse actions can also be
    attached to operator expressions. The generated parser will also
    recognize the use of parentheses to override operator precedences
    (see example below).

    Note: if you define a deep operator list, you may see performance
    issues when using infix_notation. See
    :class:`ParserElement.enable_packrat` for a mechanism to potentially
    improve your parser performance.

    Parameters:

    :param base_expr: expression representing the most basic operand to
       be used in the expression
    :param op_list: list of tuples, one for each operator precedence level
       in the expression grammar; each tuple is of the form ``(op_expr,
       num_operands, right_left_assoc, (optional)parse_action)``, where:

       - ``op_expr`` is the pyparsing expression for the operator; may also
         be a string, which will be converted to a Literal; if ``num_operands``
         is 3, ``op_expr`` is a tuple of two expressions, for the two
         operators separating the 3 terms
       - ``num_operands`` is the number of terms for this operator (must be 1,
         2, or 3)
       - ``right_left_assoc`` is the indicator whether the operator is right
         or left associative, using the pyparsing-defined constants
         ``OpAssoc.RIGHT`` and ``OpAssoc.LEFT``.
       - ``parse_action`` is the parse action to be associated with
         expressions matching this operator expression (the parse action
         tuple member may be omitted); if the parse action is passed
         a tuple or list of functions, this is equivalent to calling
         ``set_parse_action(*fn)``
         (:class:`ParserElement.set_parse_action`)

    :param lpar: expression for matching left-parentheses; if passed as a
       str, then will be parsed as ``Suppress(lpar)``. If lpar is passed as
       an expression (such as ``Literal('(')``), then it will be kept in
       the parsed results, and grouped with them. (default= ``Suppress('(')``)
    :param rpar: expression for matching right-parentheses; if passed as a
       str, then will be parsed as ``Suppress(rpar)``. If rpar is passed as
       an expression (such as ``Literal(')')``), then it will be kept in
       the parsed results, and grouped with them. (default= ``Suppress(')')``)

    Example:

    .. testcode::

       # simple example of four-function arithmetic with ints and
       # variable names
       integer = pyparsing_common.signed_integer
       varname = pyparsing_common.identifier

       arith_expr = infix_notation(integer | varname,
           [
           ('-', 1, OpAssoc.RIGHT),
           (one_of('* /'), 2, OpAssoc.LEFT),
           (one_of('+ -'), 2, OpAssoc.LEFT),
           ])

       arith_expr.run_tests('''
           5+3*6
           (5+3)*6
           (5+x)*y
           -2--11
           ''', full_dump=False)

    prints:

    .. testoutput::
       :options: +NORMALIZE_WHITESPACE


       5+3*6
       [[5, '+', [3, '*', 6]]]

       (5+3)*6
       [[[5, '+', 3], '*', 6]]

       (5+x)*y
       [[[5, '+', 'x'], '*', 'y']]

       -2--11
       [[['-', 2], '-', ['-', 11]]]
    """

    # captive version of FollowedBy that does not do parse actions or capture results names
    class _FB(FollowedBy):
        def parseImpl(self, instring, loc, doActions=True):
            self.expr.try_parse(instring, loc)
            return loc, []

    _FB.__name__ = "FollowedBy>"

    ret = Forward()
    ret.set_name(f"{base_expr.name}_expression")
    if isinstance(lpar, str):
        lpar = Suppress(lpar)
    if isinstance(rpar, str):
        rpar = Suppress(rpar)

    nested_expr = (lpar + ret + rpar).set_name(f"nested_{base_expr.name}_expression")

    # if lpar and rpar are not suppressed, wrap in group
    if not (isinstance(lpar, Suppress) and isinstance(rpar, Suppress)):
        lastExpr = base_expr | Group(nested_expr)
    else:
        lastExpr = base_expr | nested_expr

    arity: int
    rightLeftAssoc: opAssoc
    pa: typing.Optional[ParseAction]
    opExpr1: ParserElement
    opExpr2: ParserElement
    matchExpr: ParserElement
    match_lookahead: ParserElement
    for operDef in op_list:
        opExpr, arity, rightLeftAssoc, pa = (operDef + (None,))[:4]  # type: ignore[assignment]
        if isinstance(opExpr, str_type):
            opExpr = ParserElement._literalStringClass(opExpr)
        opExpr = typing.cast(ParserElement, opExpr)
        if arity == 3:
            if not isinstance(opExpr, (tuple, list)) or len(opExpr) != 2:
                raise ValueError(
                    "if numterms=3, opExpr must be a tuple or list of two expressions"
                )
            opExpr1, opExpr2 = opExpr
            term_name = f"{opExpr1}{opExpr2} operations"
        else:
            term_name = f"{opExpr} operations"

        if not 1 <= arity <= 3:
            raise ValueError("operator must be unary (1), binary (2), or ternary (3)")

        if rightLeftAssoc not in (OpAssoc.LEFT, OpAssoc.RIGHT):
            raise ValueError("operator must indicate right or left associativity")

        thisExpr: ParserElement = Forward().set_name(term_name)
        thisExpr = typing.cast(Forward, thisExpr)
        match_lookahead = And([])
        if rightLeftAssoc is OpAssoc.LEFT:
            if arity == 1:
                match_lookahead = _FB(lastExpr + opExpr)
                matchExpr = Group(lastExpr + opExpr[1, ...])
            elif arity == 2:
                if opExpr is not None:
                    match_lookahead = _FB(lastExpr + opExpr + lastExpr)
                    matchExpr = Group(lastExpr + (opExpr + lastExpr)[1, ...])
                else:
                    match_lookahead = _FB(lastExpr + lastExpr)
                    matchExpr = Group(lastExpr[2, ...])
            elif arity == 3:
                match_lookahead = _FB(
                    lastExpr + opExpr1 + lastExpr + opExpr2 + lastExpr
                )
                matchExpr = Group(
                    lastExpr + (opExpr1 + lastExpr + opExpr2 + lastExpr)[1, ...]
                )
        elif rightLeftAssoc is OpAssoc.RIGHT:
            if arity == 1:
                # try to avoid LR with this extra test
                if not isinstance(opExpr, Opt):
                    opExpr = Opt(opExpr)
                match_lookahead = _FB(opExpr.expr + thisExpr)
                matchExpr = Group(opExpr + thisExpr)
            elif arity == 2:
                if opExpr is not None:
                    match_lookahead = _FB(lastExpr + opExpr + thisExpr)
                    matchExpr = Group(lastExpr + (opExpr + thisExpr)[1, ...])
                else:
                    match_lookahead = _FB(lastExpr + thisExpr)
                    matchExpr = Group(lastExpr + thisExpr[1, ...])
            elif arity == 3:
                match_lookahead = _FB(
                    lastExpr + opExpr1 + thisExpr + opExpr2 + thisExpr
                )
                matchExpr = Group(lastExpr + opExpr1 + thisExpr + opExpr2 + thisExpr)

        # suppress lookahead expr from railroad diagrams
        match_lookahead.show_in_diagram = False

        # TODO - determine why this statement can't be included in the following
        #  if pa block
        matchExpr = match_lookahead + matchExpr

        if pa:
            if isinstance(pa, (tuple, list)):
                matchExpr.set_parse_action(*pa)
            else:
                matchExpr.set_parse_action(pa)

        thisExpr <<= (matchExpr | lastExpr).set_name(term_name)
        lastExpr = thisExpr

    ret <<= lastExpr
    return ret


def infixNotation(baseExpr, opList, lpar=Suppress('('), rpar=Suppress(')')):
    """Helper method for constructing grammars of expressions made up of
    operators working in a precedence hierarchy.  Operators may be unary
    or binary, left- or right-associative.  Parse actions can also be
    attached to operator expressions. The generated parser will also
    recognize the use of parentheses to override operator precedences
    (see example below).

    Note: if you define a deep operator list, you may see performance
    issues when using infixNotation. See
    :class:`ParserElement.enablePackrat` for a mechanism to potentially
    improve your parser performance.

    Parameters:
     - baseExpr - expression representing the most basic element for the
       nested
     - opList - list of tuples, one for each operator precedence level
       in the expression grammar; each tuple is of the form ``(opExpr,
       numTerms, rightLeftAssoc, parseAction)``, where:

       - opExpr is the pyparsing expression for the operator; may also
         be a string, which will be converted to a Literal; if numTerms
         is 3, opExpr is a tuple of two expressions, for the two
         operators separating the 3 terms
       - numTerms is the number of terms for this operator (must be 1,
         2, or 3)
       - rightLeftAssoc is the indicator whether the operator is right
         or left associative, using the pyparsing-defined constants
         ``opAssoc.RIGHT`` and ``opAssoc.LEFT``.
       - parseAction is the parse action to be associated with
         expressions matching this operator expression (the parse action
         tuple member may be omitted); if the parse action is passed
         a tuple or list of functions, this is equivalent to calling
         ``setParseAction(*fn)``
         (:class:`ParserElement.setParseAction`)
     - lpar - expression for matching left-parentheses
       (default= ``Suppress('(')``)
     - rpar - expression for matching right-parentheses
       (default= ``Suppress(')')``)

    Example::

        # simple example of four-function arithmetic with ints and
        # variable names
        integer = pyparsing_common.signed_integer
        varname = pyparsing_common.identifier

        arith_expr = infixNotation(integer | varname,
            [
            ('-', 1, opAssoc.RIGHT),
            (oneOf('* /'), 2, opAssoc.LEFT),
            (oneOf('+ -'), 2, opAssoc.LEFT),
            ])

        arith_expr.runTests('''
            5+3*6
            (5+3)*6
            -2--11
            ''', fullDump=False)

    prints::

        5+3*6
        [[5, '+', [3, '*', 6]]]

        (5+3)*6
        [[[5, '+', 3], '*', 6]]

        -2--11
        [[['-', 2], '-', ['-', 11]]]
    """
    # captive version of FollowedBy that does not do parse actions or capture results names
    class _FB(FollowedBy):
        def parseImpl(self, instring, loc, doActions=True):
            self.expr.tryParse(instring, loc)
            return loc, []

    ret = Forward()
    lastExpr = baseExpr | (lpar + ret + rpar)
    for i, operDef in enumerate(opList):
        opExpr, arity, rightLeftAssoc, pa = (operDef + (None, ))[:4]
        termName = "%s term" % opExpr if arity < 3 else "%s%s term" % opExpr
        if arity == 3:
            if opExpr is None or len(opExpr) != 2:
                raise ValueError(
                    "if numterms=3, opExpr must be a tuple or list of two expressions")
            opExpr1, opExpr2 = opExpr
        thisExpr = Forward().setName(termName)
        if rightLeftAssoc == opAssoc.LEFT:
            if arity == 1:
                matchExpr = _FB(lastExpr + opExpr) + Group(lastExpr + OneOrMore(opExpr))
            elif arity == 2:
                if opExpr is not None:
                    matchExpr = _FB(lastExpr + opExpr + lastExpr) + Group(lastExpr + OneOrMore(opExpr + lastExpr))
                else:
                    matchExpr = _FB(lastExpr + lastExpr) + Group(lastExpr + OneOrMore(lastExpr))
            elif arity == 3:
                matchExpr = (_FB(lastExpr + opExpr1 + lastExpr + opExpr2 + lastExpr)
                             + Group(lastExpr + OneOrMore(opExpr1 + lastExpr + opExpr2 + lastExpr)))
            else:
                raise ValueError("operator must be unary (1), binary (2), or ternary (3)")
        elif rightLeftAssoc == opAssoc.RIGHT:
            if arity == 1:
                # try to avoid LR with this extra test
                if not isinstance(opExpr, Optional):
                    opExpr = Optional(opExpr)
                matchExpr = _FB(opExpr.expr + thisExpr) + Group(opExpr + thisExpr)
            elif arity == 2:
                if opExpr is not None:
                    matchExpr = _FB(lastExpr + opExpr + thisExpr) + Group(lastExpr + OneOrMore(opExpr + thisExpr))
                else:
                    matchExpr = _FB(lastExpr + thisExpr) + Group(lastExpr + OneOrMore(thisExpr))
            elif arity == 3:
                matchExpr = (_FB(lastExpr + opExpr1 + thisExpr + opExpr2 + thisExpr)
                             + Group(lastExpr + opExpr1 + thisExpr + opExpr2 + thisExpr))
            else:
                raise ValueError("operator must be unary (1), binary (2), or ternary (3)")
        else:
            raise ValueError("operator must indicate right or left associativity")
        if pa:
            if isinstance(pa, (tuple, list)):
                matchExpr.setParseAction(*pa)
            else:
                matchExpr.setParseAction(pa)
        thisExpr <<= (matchExpr.setName(termName) | lastExpr)
        lastExpr = thisExpr
    ret <<= lastExpr
    return ret

