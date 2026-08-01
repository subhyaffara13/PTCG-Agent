
def test_Poly_nth():
    assert Poly(0, x).nth(0) == 0
    assert Poly(0, x).nth(1) == 0

    assert Poly(1, x).nth(0) == 1
    assert Poly(1, x).nth(1) == 0

    assert Poly(x**8, x).nth(0) == 0
    assert Poly(x**8, x).nth(7) == 0
    assert Poly(x**8, x).nth(8) == 1
    assert Poly(x**8, x).nth(9) == 0

    assert Poly(3*x*y**2 + 1, x, y).nth(0, 0) == 1
    assert Poly(3*x*y**2 + 1, x, y).nth(1, 2) == 3

    raises(ValueError, lambda: Poly(x*y + 1, x, y).nth(1))

