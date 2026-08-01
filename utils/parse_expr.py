
def parse_expr(s, local_dict):
    """
    Converts the string "s" to a SymPy expression, in local_dict.

    It converts all numbers to Integers before feeding it to Python and
    automatically creates Symbols.
    """
    global_dict = {}
    exec('from sympy import *', global_dict)
    try:
        a = parse(s.strip(), mode="eval")
    except SyntaxError:
        raise SympifyError("Cannot parse %s." % repr(s))
    a = Transform(local_dict, global_dict).visit(a)
    e = compile(a, "<string>", "eval")
    return eval(e, global_dict, local_dict)


def parse_expr(s: str, local_dict: DICT | None = None,
               transformations: tuple[TRANS, ...] | str \
                   = standard_transformations,
               global_dict: DICT | None = None, evaluate=True):
    """Converts the string ``s`` to a SymPy expression, in ``local_dict``.

    .. warning::
        Note that this function uses ``eval``, and thus shouldn't be used on
        unsanitized input.

    Parameters
    ==========

    s : str
        The string to parse.

    local_dict : dict, optional
        A dictionary of local variables to use when parsing.

    global_dict : dict, optional
        A dictionary of global variables. By default, this is initialized
        with ``from sympy import *``; provide this parameter to override
        this behavior (for instance, to parse ``"Q & S"``).

    transformations : tuple or str
        A tuple of transformation functions used to modify the tokens of the
        parsed expression before evaluation. The default transformations
        convert numeric literals into their SymPy equivalents, convert
        undefined variables into SymPy symbols, and allow the use of standard
        mathematical factorial notation (e.g. ``x!``). Selection via
        string is available (see below).

    evaluate : bool, optional
        When False, the order of the arguments will remain as they were in the
        string and automatic simplification that would normally occur is
        suppressed. (see examples)

    Examples
    ========

    >>> from sympy.parsing.sympy_parser import parse_expr
    >>> parse_expr("1/2")
    1/2
    >>> type(_)
    <class 'sympy.core.numbers.Half'>
    >>> from sympy.parsing.sympy_parser import standard_transformations,\\
    ... implicit_multiplication_application
    >>> transformations = (standard_transformations +
    ...     (implicit_multiplication_application,))
    >>> parse_expr("2x", transformations=transformations)
    2*x

    When evaluate=False, some automatic simplifications will not occur:

    >>> parse_expr("2**3"), parse_expr("2**3", evaluate=False)
    (8, 2**3)

    In addition the order of the arguments will not be made canonical.
    This feature allows one to tell exactly how the expression was entered:

    >>> a = parse_expr('1 + x', evaluate=False)
    >>> b = parse_expr('x + 1', evaluate=False)
    >>> a == b
    False
    >>> a.args
    (1, x)
    >>> b.args
    (x, 1)

    Note, however, that when these expressions are printed they will
    appear the same:

    >>> assert str(a) == str(b)

    As a convenience, transformations can be seen by printing ``transformations``:

    >>> from sympy.parsing.sympy_parser import transformations

    >>> print(transformations)
    0: lambda_notation
    1: auto_symbol
    2: repeated_decimals
    3: auto_number
    4: factorial_notation
    5: implicit_multiplication_application
    6: convert_xor
    7: implicit_application
    8: implicit_multiplication
    9: convert_equals_signs
    10: function_exponentiation
    11: rationalize

    The ``T`` object provides a way to select these transformations:

    >>> from sympy.parsing.sympy_parser import T

    If you print it, you will see the same list as shown above.

    >>> str(T) == str(transformations)
    True

    Standard slicing will return a tuple of transformations:

    >>> T[:5] == standard_transformations
    True

    So ``T`` can be used to specify the parsing transformations:

    >>> parse_expr("2x", transformations=T[:5])
    Traceback (most recent call last):
    ...
    SyntaxError: invalid syntax
    >>> parse_expr("2x", transformations=T[:6])
    2*x
    >>> parse_expr('.3', transformations=T[3, 11])
    3/10
    >>> parse_expr('.3x', transformations=T[:])
    3*x/10

    As a further convenience, strings 'implicit' and 'all' can be used
    to select 0-5 and all the transformations, respectively.

    >>> parse_expr('.3x', transformations='all')
    3*x/10

    See Also
    ========

    stringify_expr, eval_expr, standard_transformations,
    implicit_multiplication_application

    """

    if local_dict is None:
        local_dict = {}
    elif not isinstance(local_dict, dict):
        raise TypeError('expecting local_dict to be a dict')
    elif null in local_dict:
        raise ValueError('cannot use "" in local_dict')

    if global_dict is None:
        global_dict = {}
        exec('from sympy import *', global_dict)

        builtins_dict = vars(builtins)
        for name, obj in builtins_dict.items():
            if isinstance(obj, types.BuiltinFunctionType):
                global_dict[name] = obj
        global_dict['max'] = Max
        global_dict['min'] = Min

    elif not isinstance(global_dict, dict):
        raise TypeError('expecting global_dict to be a dict')

    transformations = transformations or ()
    if isinstance(transformations, str):
        if transformations == 'all':
            _transformations = T[:]
        elif transformations == 'implicit':
            _transformations = T[:6]
        else:
            raise ValueError('unknown transformation group name')
    else:
        _transformations = transformations

    code = stringify_expr(s, local_dict, global_dict, _transformations)

    if not evaluate:
        code = compile(evaluateFalse(code), '<string>', 'eval') # type: ignore

    try:
        rv = eval_expr(code, local_dict, global_dict)
        # restore neutral definitions for names
        for i in local_dict.pop(null, ()):
            local_dict[i] = null
        return rv
    except Exception as e:
        # restore neutral definitions for names
        for i in local_dict.pop(null, ()):
            local_dict[i] = null
        raise e from ValueError(f"Error from parse_expr with transformed code: {code!r}")

