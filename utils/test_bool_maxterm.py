
def test_bool_maxterm():
    x, y = symbols('x,y')
    assert bool_maxterm(2, [x, y]) == Or(Not(x), y)
    assert bool_maxterm([0, 1], [x, y]) == Or(Not(y), x)

