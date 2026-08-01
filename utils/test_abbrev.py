
def test_abbrev():
    u = Quantity("u")
    u.set_global_relative_scale_factor(S.One, meter)

    assert u.name == Symbol("u")
    assert u.abbrev == Symbol("u")

    u = Quantity("u", abbrev="om")
    u.set_global_relative_scale_factor(S(2), meter)

    assert u.name == Symbol("u")
    assert u.abbrev == Symbol("om")
    assert u.scale_factor == 2
    assert isinstance(u.scale_factor, Number)

    u = Quantity("u", abbrev="ikm")
    u.set_global_relative_scale_factor(3*kilo, meter)

    assert u.abbrev == Symbol("ikm")
    assert u.scale_factor == 3000

