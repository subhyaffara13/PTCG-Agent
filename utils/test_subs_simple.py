
def test_subs_simple():
    a = symbols('a', commutative=True)
    x = symbols('x', commutative=False)

    assert (2*a).subs(1, 3) == 2*a
    assert (2*a).subs(2, 3) == 3*a
    assert (2*a).subs(a, 3) == 6
    assert sin(2).subs(1, 3) == sin(2)
    assert sin(2).subs(2, 3) == sin(3)
    assert sin(a).subs(a, 3) == sin(3)

    assert (2*x).subs(1, 3) == 2*x
    assert (2*x).subs(2, 3) == 3*x
    assert (2*x).subs(x, 3) == 6
    assert sin(x).subs(x, 3) == sin(3)

