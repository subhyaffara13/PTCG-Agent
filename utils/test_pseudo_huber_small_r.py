
def test_pseudo_huber_small_r():
    delta = 1.0
    r = 1e-18
    y = special.pseudo_huber(delta, r)
    # expected computed with mpmath:
    #     import mpmath
    #     mpmath.mp.dps = 200
    #     r = mpmath.mpf(1e-18)
    #     expected = float(mpmath.sqrt(1 + r**2) - 1)
    expected = 5.0000000000000005e-37
    assert_allclose(y, expected, rtol=1e-13)

