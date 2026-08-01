
def test_find_reasonable_pivot_naive_finds_guaranteed_nonzero2():
    # Test if matrices._find_reasonable_pivot_naive()
    # finds a guaranteed non-zero pivot when the
    # some of the candidate pivots are symbolic expressions.
    # Keyword argument: simpfunc=_simplify indicates that the search
    # should attempt to simplify candidate pivots.
    x = Symbol('x')
    column = Matrix(3, 1,
                    [x,
                     cos(x)**2+sin(x)**2+x**2,
                     cos(x)**2+sin(x)**2])
    pivot_offset, pivot_val, pivot_assumed_nonzero, simplified =\
        _find_reasonable_pivot_naive(column, simpfunc=_simplify)
    assert pivot_val == 1


def test_find_reasonable_pivot_naive_finds_guaranteed_nonzero2():
    # Test if matrices._find_reasonable_pivot_naive()
    # finds a guaranteed non-zero pivot when the
    # some of the candidate pivots are symbolic expressions.
    # Keyword argument: simpfunc=_simplify indicates that the search
    # should attempt to simplify candidate pivots.
    x = Symbol('x')
    column = Matrix(3, 1,
                    [x,
                     cos(x)**2+sin(x)**2+x**2,
                     cos(x)**2+sin(x)**2])
    pivot_offset, pivot_val, pivot_assumed_nonzero, simplified =\
        _find_reasonable_pivot_naive(column, simpfunc=_simplify)
    assert pivot_val == 1

