
def test_has_integrals():
    f = Integral(x**2 + sin(x*y*z), (x, 0, x + y + z))

    assert f.has(x + y)
    assert f.has(x + z)
    assert f.has(y + z)

    assert f.has(x*y)
    assert f.has(x*z)
    assert f.has(y*z)

    assert not f.has(2*x + y)
    assert not f.has(2*x*y)

