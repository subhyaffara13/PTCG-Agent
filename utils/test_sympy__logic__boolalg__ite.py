
def test_sympy__logic__boolalg__ITE():
    from sympy.logic.boolalg import ITE
    assert _test_args(ITE(x, y, 1))

