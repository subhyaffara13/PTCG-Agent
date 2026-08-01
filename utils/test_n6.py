
def test_N6():
    x, y, k, n = symbols('x y k n', real=True)
    assert ask(k*x**n > k*y**n, (x > y) & (y > 0) & (k > 0) & (n > 0)) is True

