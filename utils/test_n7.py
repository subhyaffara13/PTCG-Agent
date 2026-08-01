
def test_N7():
    x, y = symbols('x y', real=True)
    assert ask(y > 0, (x > 1) & (y >= x - 1)) is True

