
def test_requires_partial_unspecified_variables():
    x, y = symbols('x y')
    # function of unspecified variables
    f = symbols('f', cls=Function)
    assert requires_partial(Derivative(f, x)) is False
    assert requires_partial(Derivative(f, x, y)) is True

