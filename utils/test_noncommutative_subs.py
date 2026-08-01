
def test_noncommutative_subs():
    x,y = symbols('x,y', commutative=False)
    assert (x*y*x).subs([(x, x*y), (y, x)], simultaneous=True) == (x*y*x**2*y)

