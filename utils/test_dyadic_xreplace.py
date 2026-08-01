
def test_dyadic_xreplace():
    x, y, z = symbols('x y z')
    N = ReferenceFrame('N')
    D = outer(N.x, N.x)
    v = x*y * D
    assert v.xreplace({x : cos(x)}) == cos(x)*y * D
    assert v.xreplace({x*y : pi}) == pi * D
    v = (x*y)**z * D
    assert v.xreplace({(x*y)**z : 1}) == D
    assert v.xreplace({x:1, z:0}) == D
    raises(TypeError, lambda: v.xreplace())
    raises(TypeError, lambda: v.xreplace([x, y]))

