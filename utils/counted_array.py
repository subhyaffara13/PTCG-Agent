
def counted_array(
    expr: ParserElement, int_expr: typing.Optional[ParserElement] = None, **kwargs
) -> ParserElement:
    """Helper to define a counted list of expressions.

    This helper defines a pattern of the form::

        integer expr expr expr...

    where the leading integer tells how many expr expressions follow.
    The matched tokens returns the array of expr tokens as a list - the
    leading count token is suppressed.

    If ``int_expr`` is specified, it should be a pyparsing expression
    that produces an integer value.

    Examples:

    .. doctest::

        >>> counted_array(Word(alphas)).parse_string('2 ab cd ef')
        ParseResults(['ab', 'cd'], {})

    - In this parser, the leading integer value is given in binary,
      '10' indicating that 2 values are in the array:

      .. doctest::

        >>> binary_constant = Word('01').set_parse_action(lambda t: int(t[0], 2))
        >>> counted_array(Word(alphas), int_expr=binary_constant
        ...     ).parse_string('10 ab cd ef')
        ParseResults(['ab', 'cd'], {})

    - If other fields must be parsed after the count but before the
      list items, give the fields results names and they will
      be preserved in the returned ParseResults:

      .. doctest::

         >>> ppc = pyparsing.common
         >>> count_with_metadata = ppc.integer + Word(alphas)("type")
         >>> typed_array = counted_array(Word(alphanums),
         ...     int_expr=count_with_metadata)("items")
         >>> result = typed_array.parse_string("3 bool True True False")
         >>> print(result.dump())
         ['True', 'True', 'False']
         - items: ['True', 'True', 'False']
         - type: 'bool'
    """
    intExpr: typing.Optional[ParserElement] = deprecate_argument(
        kwargs, "intExpr", None
    )

    intExpr = intExpr or int_expr
    array_expr = Forward()

    def count_field_parse_action(s, l, t):
        nonlocal array_expr
        n = t[0]
        array_expr <<= (expr * n) if n else Empty()
        # clear list contents, but keep any named results
        del t[:]

    if intExpr is None:
        intExpr = Word(nums).set_parse_action(lambda t: int(t[0]))
    else:
        intExpr = intExpr.copy()
    intExpr.set_name("arrayLen")
    intExpr.add_parse_action(count_field_parse_action, call_during_try=True)
    return (intExpr + array_expr).set_name(f"(len) {expr}...")


def countedArray(expr, intExpr=None):
    """Helper to define a counted list of expressions.

    This helper defines a pattern of the form::

        integer expr expr expr...

    where the leading integer tells how many expr expressions follow.
    The matched tokens returns the array of expr tokens as a list - the
    leading count token is suppressed.

    If ``intExpr`` is specified, it should be a pyparsing expression
    that produces an integer value.

    Example::

        countedArray(Word(alphas)).parseString('2 ab cd ef')  # -> ['ab', 'cd']

        # in this parser, the leading integer value is given in binary,
        # '10' indicating that 2 values are in the array
        binaryConstant = Word('01').setParseAction(lambda t: int(t[0], 2))
        countedArray(Word(alphas), intExpr=binaryConstant).parseString('10 ab cd ef')  # -> ['ab', 'cd']
    """
    arrayExpr = Forward()
    def countFieldParseAction(s, l, t):
        n = t[0]
        arrayExpr << (n and Group(And([expr] * n)) or Group(empty))
        return []
    if intExpr is None:
        intExpr = Word(nums).setParseAction(lambda t: int(t[0]))
    else:
        intExpr = intExpr.copy()
    intExpr.setName("arrayLen")
    intExpr.addParseAction(countFieldParseAction, callDuringTry=True)
    return (intExpr + arrayExpr).setName('(len) ' + _ustr(expr) + '...')

