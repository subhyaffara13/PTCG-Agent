
def test_wigner():
    try:
        import numpy as np
    except ImportError:
        skip("numpy not installed")
    def tn(a, b):
        return (a - b).n(64) < S('1e-64')
    assert tn(wigner_9j(1, 1, 1, 1, 1, 1, 1, 1, 0, prec=64), Rational(1, 18))
    assert wigner_9j(3, 3, 2, 3, 3, 2, 3, 3, 2) == 3221*sqrt(
        70)/(246960*sqrt(105)) - 365/(3528*sqrt(70)*sqrt(105))
    assert wigner_6j(5, 5, 5, 5, 5, 5) == Rational(1, 52)
    assert tn(wigner_6j(8, 8, 8, 8, 8, 8, prec=64), Rational(-12219, 965770))
    assert wigner_6j(1, 1, 1, 1.0, np.float64(1.0), 1) == Rational(1, 6)
    assert wigner_6j(3.0, np.float32(3), 3.0, 3, 3, 3) == Rational(-1, 14)
    # regression test for #8747
    half = S.Half
    assert wigner_9j(0, 0, 0, 0, half, half, 0, half, half) == half
    assert (wigner_9j(3, 5, 4,
                      7 * half, 5 * half, 4,
                      9 * half, 9 * half, 0)
            == -sqrt(Rational(361, 205821000)))
    assert (wigner_9j(1, 4, 3,
                      5 * half, 4, 5 * half,
                      5 * half, 2, 7 * half)
            == -sqrt(Rational(3971, 373403520)))
    assert (wigner_9j(4, 9 * half, 5 * half,
                      2, 4, 4,
                      5, 7 * half, 7 * half)
            == -sqrt(Rational(3481, 5042614500)))
    assert (wigner_9j(5, 5, 5.0,
                      np.float64(5.0), 5, 5,
                      5, 5, 5)
            == 0)
    assert (wigner_9j(1.0, 2.0, 3.0,
                      3, 2, 1,
                      2, 1, 3)
            == -4*sqrt(70)/11025)

