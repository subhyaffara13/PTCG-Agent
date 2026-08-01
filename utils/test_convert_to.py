
def test_convert_to():
    q = Quantity("q1")
    q.set_global_relative_scale_factor(S(5000), meter)

    assert q.convert_to(m) == 5000*m

    assert speed_of_light.convert_to(m / s) == 299792458 * m / s
    assert day.convert_to(s) == 86400*s

    # Wrong dimension to convert:
    assert q.convert_to(s) == q
    assert speed_of_light.convert_to(m) == speed_of_light

    expr = joule*second
    conv = convert_to(expr, joule)
    assert conv == joule*second


def test_convert_to():
    A = Quantity("A")
    A.set_global_relative_scale_factor(S.One, ampere)

    Js = Quantity("Js")
    Js.set_global_relative_scale_factor(S.One, joule*second)

    mksa = UnitSystem((m, kg, s, A), (Js,))
    assert convert_to(Js, mksa._base_units) == m**2*kg*s**-1/1000

