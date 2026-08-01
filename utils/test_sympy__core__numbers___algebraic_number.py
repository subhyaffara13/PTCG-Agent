
def test_sympy__core__numbers__AlgebraicNumber():
    from sympy.core.numbers import AlgebraicNumber
    assert _test_args(AlgebraicNumber(sqrt(2), [1, 2, 3]))

