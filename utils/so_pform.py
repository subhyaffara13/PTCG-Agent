
def SOPform(variables, minterms, dontcares=None):
    """
    The SOPform function uses simplified_pairs and a redundant group-
    eliminating algorithm to convert the list of all input combos that
    generate '1' (the minterms) into the smallest sum-of-products form.

    The variables must be given as the first argument.

    Return a logical :py:class:`~.Or` function (i.e., the "sum of products" or
    "SOP" form) that gives the desired outcome. If there are inputs that can
    be ignored, pass them as a list, too.

    The result will be one of the (perhaps many) functions that satisfy
    the conditions.

    Examples
    ========

    >>> from sympy.logic import SOPform
    >>> from sympy import symbols
    >>> w, x, y, z = symbols('w x y z')
    >>> minterms = [[0, 0, 0, 1], [0, 0, 1, 1],
    ...             [0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 1, 1]]
    >>> dontcares = [[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 1]]
    >>> SOPform([w, x, y, z], minterms, dontcares)
    (y & z) | (~w & ~x)

    The terms can also be represented as integers:

    >>> minterms = [1, 3, 7, 11, 15]
    >>> dontcares = [0, 2, 5]
    >>> SOPform([w, x, y, z], minterms, dontcares)
    (y & z) | (~w & ~x)

    They can also be specified using dicts, which does not have to be fully
    specified:

    >>> minterms = [{w: 0, x: 1}, {y: 1, z: 1, x: 0}]
    >>> SOPform([w, x, y, z], minterms)
    (x & ~w) | (y & z & ~x)

    Or a combination:

    >>> minterms = [4, 7, 11, [1, 1, 1, 1]]
    >>> dontcares = [{w : 0, x : 0, y: 0}, 5]
    >>> SOPform([w, x, y, z], minterms, dontcares)
    (w & y & z) | (~w & ~y) | (x & z & ~w)

    See also
    ========

    POSform

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Quine-McCluskey_algorithm
    .. [2] https://en.wikipedia.org/wiki/Don%27t-care_term

    """
    if not minterms:
        return false

    variables = tuple(map(sympify, variables))


    minterms = _input_to_binlist(minterms, variables)
    dontcares = _input_to_binlist((dontcares or []), variables)
    for d in dontcares:
        if d in minterms:
            raise ValueError('%s in minterms is also in dontcares' % d)

    return _sop_form(variables, minterms, dontcares)

