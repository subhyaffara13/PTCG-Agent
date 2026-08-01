
def test_subs_constants():
    a, b = symbols('a b', commutative=True)
    x, y = symbols('x y', commutative=False)

    assert (a*b).subs(2*a, 1) == a*b
    assert (1.5*a*b).subs(a, 1) == 1.5*b
    assert (2*a*b).subs(2*a, 1) == b
    assert (2*a*b).subs(4*a, 1) == 2*a*b

    assert (x*y).subs(2*x, 1) == x*y
    assert (1.5*x*y).subs(x, 1) == 1.5*y
    assert (2*x*y).subs(2*x, 1) == y
    assert (2*x*y).subs(4*x, 1) == 2*x*y

