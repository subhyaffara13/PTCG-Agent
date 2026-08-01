
def test_N8():
    x, y, z = symbols('x y z', real=True)
    assert ask(Eq(x, y) & Eq(y, z),
               (x >= y) & (y >= z) & (z >= x))

