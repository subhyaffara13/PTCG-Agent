
def test_W26():
    x, y = symbols('x y', real=True)
    assert integrate(integrate(abs(y - x**2), (y, 0, 2)),
                     (x, -1, 1)) == R(46, 15)

