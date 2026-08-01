
def test_Poly_homogeneous_order():
    assert Poly(0, x, y).homogeneous_order() is -oo
    assert Poly(1, x, y).homogeneous_order() == 0
    assert Poly(x, x, y).homogeneous_order() == 1
    assert Poly(x*y, x, y).homogeneous_order() == 2

    assert Poly(x + 1, x, y).homogeneous_order() is None
    assert Poly(x*y + x, x, y).homogeneous_order() is None

    assert Poly(x**5 + 2*x**3*y**2 + 9*x*y**4).homogeneous_order() == 5
    assert Poly(x**5 + 2*x**3*y**3 + 9*x*y**4).homogeneous_order() is None

