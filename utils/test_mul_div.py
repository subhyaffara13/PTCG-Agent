
def test_mul_div():
    u = Quantity("u")
    v = Quantity("v")
    t = Quantity("t")
    ut = Quantity("ut")
    v2 = Quantity("v")

    u.set_global_relative_scale_factor(S(10), meter)
    v.set_global_relative_scale_factor(S(5), meter)
    t.set_global_relative_scale_factor(S(2), second)
    ut.set_global_relative_scale_factor(S(20), meter*second)
    v2.set_global_relative_scale_factor(S(5), meter/second)

    assert 1 / u == u**(-1)
    assert u / 1 == u

    v1 = u / t
    v2 = v

    # Pow only supports structural equality:
    assert v1 != v2
    assert v1 == v2.convert_to(v1)

    # TODO: decide whether to allow such expression in the future
    # (requires somehow manipulating the core).
    # assert u / Quantity('l2', dimension=length, scale_factor=2) == 5

    assert u * 1 == u

    ut1 = u * t
    ut2 = ut

    # Mul only supports structural equality:
    assert ut1 != ut2
    assert ut1 == ut2.convert_to(ut1)

    # Mul only supports structural equality:
    lp1 = Quantity("lp1")
    lp1.set_global_relative_scale_factor(S(2), 1/meter)
    assert u * lp1 != 20

    assert u**0 == 1
    assert u**1 == u

    # TODO: Pow only support structural equality:
    u2 = Quantity("u2")
    u3 = Quantity("u3")
    u2.set_global_relative_scale_factor(S(100), meter**2)
    u3.set_global_relative_scale_factor(Rational(1, 10), 1/meter)

    assert u ** 2 != u2
    assert u ** -1 != u3

    assert u ** 2 == u2.convert_to(u)
    assert u ** -1 == u3.convert_to(u)

