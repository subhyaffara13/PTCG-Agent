
def test_evalf_power_subs_bugs():
    assert (x**2).evalf(subs={x: 0}) == 0
    assert sqrt(x).evalf(subs={x: 0}) == 0
    assert (x**Rational(2, 3)).evalf(subs={x: 0}) == 0
    assert (x**x).evalf(subs={x: 0}) == 1.0
    assert (3**x).evalf(subs={x: 0}) == 1.0
    assert exp(x).evalf(subs={x: 0}) == 1.0
    assert ((2 + I)**x).evalf(subs={x: 0}) == 1.0
    assert (0**x).evalf(subs={x: 0}) == 1.0

