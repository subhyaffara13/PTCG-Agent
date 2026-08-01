
def test_find_reasonable_pivot_naive_simplifies():
    # Test if matrices._find_reasonable_pivot_naive()
    # simplifies candidate pivots, and reports
    # their offsets correctly.
    x = Symbol('x')
    column = Matrix(3, 1,
                    [x,
                     cos(x)**2+sin(x)**2+x,
                     cos(x)**2+sin(x)**2])
    pivot_offset, pivot_val, pivot_assumed_nonzero, simplified =\
        _find_reasonable_pivot_naive(column, simpfunc=_simplify)

    assert len(simplified) == 2
    assert simplified[0][0] == 1
    assert simplified[0][1] == 1+x
    assert simplified[1][0] == 2
    assert simplified[1][1] == 1


def test_find_reasonable_pivot_naive_simplifies():
    # Test if matrices._find_reasonable_pivot_naive()
    # simplifies candidate pivots, and reports
    # their offsets correctly.
    x = Symbol('x')
    column = Matrix(3, 1,
                    [x,
                     cos(x)**2+sin(x)**2+x,
                     cos(x)**2+sin(x)**2])
    pivot_offset, pivot_val, pivot_assumed_nonzero, simplified =\
        _find_reasonable_pivot_naive(column, simpfunc=_simplify)

    assert len(simplified) == 2
    assert simplified[0][0] == 1
    assert simplified[0][1] == 1+x
    assert simplified[1][0] == 2
    assert simplified[1][1] == 1

