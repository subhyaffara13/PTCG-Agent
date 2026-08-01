
def test_sympy__logic__boolalg__And():
    from sympy.logic.boolalg import And
    assert _test_args(And(x, y, 1))

