
def test_find_reasonable_pivot_naive_finds_guaranteed_nonzero1():
    # Test if matrices._find_reasonable_pivot_naive()
    # finds a guaranteed non-zero pivot when the
    # some of the candidate pivots are symbolic expressions.
    # Keyword argument: simpfunc=None indicates that no simplifications
    # should be performed during the search.
    x = Symbol('x')
    column = Matrix(3, 1, [x, cos(x)**2 + sin(x)**2, S.Half])
    pivot_offset, pivot_val, pivot_assumed_nonzero, simplified =\
        _find_reasonable_pivot_naive(column)
    assert pivot_val == S.Half


def test_find_reasonable_pivot_naive_finds_guaranteed_nonzero1():
    # Test if matrices._find_reasonable_pivot_naive()
    # finds a guaranteed non-zero pivot when the
    # some of the candidate pivots are symbolic expressions.
    # Keyword argument: simpfunc=None indicates that no simplifications
    # should be performed during the search.
    x = Symbol('x')
    column = Matrix(3, 1, [x, cos(x)**2 + sin(x)**2, S.Half])
    pivot_offset, pivot_val, pivot_assumed_nonzero, simplified =\
        _find_reasonable_pivot_naive(column)
    assert pivot_val == S.Half

