
def test_M35():
    x, y = symbols('x y', real=True)
    assert linsolve((3*x - 2*y - I*y + 3*I).as_real_imag(), y, x) == FiniteSet((3, 2))

