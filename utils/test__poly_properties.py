
def test_Poly_properties():
    assert Poly(0, x).is_zero is True
    assert Poly(1, x).is_zero is False

    assert Poly(1, x).is_one is True
    assert Poly(2, x).is_one is False

    assert Poly(x - 1, x).is_sqf is True
    assert Poly((x - 1)**2, x).is_sqf is False

    assert Poly(x - 1, x).is_monic is True
    assert Poly(2*x - 1, x).is_monic is False

    assert Poly(3*x + 2, x).is_primitive is True
    assert Poly(4*x + 2, x).is_primitive is False

    assert Poly(1, x).is_ground is True
    assert Poly(x, x).is_ground is False

    assert Poly(x + y + z + 1).is_linear is True
    assert Poly(x*y*z + 1).is_linear is False

    assert Poly(x*y + z + 1).is_quadratic is True
    assert Poly(x*y*z + 1).is_quadratic is False

    assert Poly(x*y).is_monomial is True
    assert Poly(x*y + 1).is_monomial is False

    assert Poly(x**2 + x*y).is_homogeneous is True
    assert Poly(x**3 + x*y).is_homogeneous is False

    assert Poly(x).is_univariate is True
    assert Poly(x*y).is_univariate is False

    assert Poly(x*y).is_multivariate is True
    assert Poly(x).is_multivariate is False

    assert Poly(
        x**16 + x**14 - x**10 + x**8 - x**6 + x**2 + 1).is_cyclotomic is False
    assert Poly(
        x**16 + x**14 - x**10 - x**8 - x**6 + x**2 + 1).is_cyclotomic is True

