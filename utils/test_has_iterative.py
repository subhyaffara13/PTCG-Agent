
def test_has_iterative():
    A, B, C = symbols('A,B,C', commutative=False)
    f = x*gamma(x)*sin(x)*exp(x*y)*A*B*C*cos(x*A*B)

    assert f.has(x)
    assert f.has(x*y)
    assert f.has(x*sin(x))
    assert not f.has(x*sin(y))
    assert f.has(x*A)
    assert f.has(x*A*B)
    assert not f.has(x*A*C)
    assert f.has(x*A*B*C)
    assert not f.has(x*A*C*B)
    assert f.has(x*sin(x)*A*B*C)
    assert not f.has(x*sin(x)*A*C*B)
    assert not f.has(x*sin(y)*A*B*C)
    assert f.has(x*gamma(x))
    assert not f.has(x + sin(x))

    assert (x & y & z).has(x & z)

