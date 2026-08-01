
def test_N4():
    x, y = symbols('x y', real=True)
    assert ask(2*x**2 > 2*y**2, (x > y) & (y > 0)) is True

