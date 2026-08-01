
def test_N3():
    x = symbols('x', real=True)
    assert ask(And(Lt(-1, x), Lt(x, 1)), abs(x) < 1 )

