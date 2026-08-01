
def test_bool_monomial():
    x, y = symbols('x,y')
    assert bool_monomial(1, [x, y]) == y
    assert bool_monomial([1, 1], [x, y]) == And(x, y)

