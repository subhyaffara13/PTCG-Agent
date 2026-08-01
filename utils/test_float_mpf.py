
def test_float_mpf():
    import mpmath
    mpmath.mp.dps = 100
    mp_pi = mpmath.pi()

    assert Float(mp_pi, 100) == Float(mp_pi._mpf_, 100) == pi.evalf(100)

    mpmath.mp.dps = 15

    assert Float(mp_pi, 100) == Float(mp_pi._mpf_, 100) == pi.evalf(100)

