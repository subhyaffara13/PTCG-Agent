
def test_FracElement_subs():
    F, x,y,z = field("x,y,z", ZZ)
    f = (x**2 + 3*y)/z

    assert f.subs(x, 0) == 3*y/z
    raises(ZeroDivisionError, lambda: f.subs(z, 0))

