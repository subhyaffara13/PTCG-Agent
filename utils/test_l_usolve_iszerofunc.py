
def test_LUsolve_iszerofunc():
    # taken from https://github.com/sympy/sympy/issues/24679

    M = Matrix([[(x + 1)**2 - (x**2 + 2*x + 1), x], [x, 0]])
    b = Matrix([1, 1])
    is_zero_func = lambda e: False if e._random() else True

    x_exp = Matrix([1/x, (1-(-x**2 - 2*x + (x+1)**2 - 1)/x)/x])

    assert (x_exp - M.LUsolve(b, iszerofunc=is_zero_func)) == Matrix([0, 0])

