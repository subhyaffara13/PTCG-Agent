
def test_bugs():
    from sympy.functions.elementary.complexes import (polar_lift, re)

    assert abs(re((1 + I)**2)) < 1e-15

    # anything that evalf's to 0 will do in place of polar_lift
    assert abs(polar_lift(0)).n() == 0


def test_bugs():
    # particular bugs
    assert mpf(4.4408920985006262E-16) < mpf(1.7763568394002505E-15)
    assert mpf(-4.4408920985006262E-16) > mpf(-1.7763568394002505E-15)

