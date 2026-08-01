
def test_spherical_bessel_fn():
    x, z = symbols("x z")
    assert spherical_bessel_fn(1, z) == 1/z**2
    assert spherical_bessel_fn(2, z) == -1/z + 3/z**3
    assert spherical_bessel_fn(3, z) == -6/z**2 + 15/z**4
    assert spherical_bessel_fn(4, z) == 1/z - 45/z**3 + 105/z**5

