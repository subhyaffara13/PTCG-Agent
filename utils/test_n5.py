
def test_N5():
    x, y, k = symbols('x y k', real=True)
    assert ask(k*x**2 > k*y**2, (x > y) & (y > 0) & (k > 0)) is True

