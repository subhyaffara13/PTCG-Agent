
def test_bessel_functions_at_infinity():
    # Pull Request 23844 implements limits for all bessel and modified bessel
    # functions approaching infinity along any direction i.e. abs(z0) tends to oo

    assert limit(besselj(1, x), x, oo) == 0
    assert limit(besselj(1, x), x, -oo) == 0
    assert limit(besselj(1, x), x, I*oo) == oo*I
    assert limit(besselj(1, x), x, -I*oo) == -oo*I
    assert limit(bessely(1, x), x, oo) == 0
    assert limit(bessely(1, x), x, -oo) == 0
    assert limit(bessely(1, x), x, I*oo) == -oo
    assert limit(bessely(1, x), x, -I*oo) == -oo
    assert limit(besseli(1, x), x, oo) == oo
    assert limit(besseli(1, x), x, -oo) == -oo
    assert limit(besseli(1, x), x, I*oo) == 0
    assert limit(besseli(1, x), x, -I*oo) == 0
    assert limit(besselk(1, x), x, oo) == 0
    assert limit(besselk(1, x), x, -oo) == -oo*I
    assert limit(besselk(1, x), x, I*oo) == 0
    assert limit(besselk(1, x), x, -I*oo) == 0

    # test issue 14874
    assert limit(besselk(0, x), x, oo) == 0

