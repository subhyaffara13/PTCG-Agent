
def test_Poly_slice():
    f = Poly(x**3 + 2*x**2 + 3*x + 4)

    assert f.slice(0, 0) == Poly(0, x)
    assert f.slice(0, 1) == Poly(4, x)
    assert f.slice(0, 2) == Poly(3*x + 4, x)
    assert f.slice(0, 3) == Poly(2*x**2 + 3*x + 4, x)
    assert f.slice(0, 4) == Poly(x**3 + 2*x**2 + 3*x + 4, x)

    assert f.slice(x, 0, 0) == Poly(0, x)
    assert f.slice(x, 0, 1) == Poly(4, x)
    assert f.slice(x, 0, 2) == Poly(3*x + 4, x)
    assert f.slice(x, 0, 3) == Poly(2*x**2 + 3*x + 4, x)
    assert f.slice(x, 0, 4) == Poly(x**3 + 2*x**2 + 3*x + 4, x)

    g = Poly(x**3 + 1)

    assert g.slice(0, 3) == Poly(1, x)

