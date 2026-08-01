
def test_bool_minterm():
    x, y = symbols('x,y')
    assert bool_minterm(3, [x, y]) == And(x, y)
    assert bool_minterm([1, 0], [x, y]) == And(Not(y), x)

