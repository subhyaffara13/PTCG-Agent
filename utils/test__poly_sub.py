
def test_Poly_sub():
    assert Poly(0, x).sub(Poly(0, x)) == Poly(0, x)
    assert Poly(0, x) - Poly(0, x) == Poly(0, x)

    assert Poly(1, x).sub(Poly(0, x)) == Poly(1, x)
    assert Poly(1, x, y) - Poly(0, x) == Poly(1, x, y)
    assert Poly(0, x).sub(Poly(1, x, y)) == Poly(-1, x, y)
    assert Poly(0, x, y) - Poly(1, x, y) == Poly(-1, x, y)

    assert Poly(1, x) - x == Poly(1 - x, x)
    with warns_deprecated_sympy():
        Poly(1, x) - sin(x)

    assert Poly(x, x) - 1 == Poly(x - 1, x)
    assert 1 - Poly(x, x) == Poly(1 - x, x)

