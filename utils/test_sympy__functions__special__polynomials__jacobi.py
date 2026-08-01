
def test_sympy__functions__special__polynomials__jacobi():
    from sympy.functions.special.polynomials import jacobi
    assert _test_args(jacobi(x, y, 2, 2))

