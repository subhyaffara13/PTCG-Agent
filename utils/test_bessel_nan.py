
def test_bessel_nan():
    # FIXME: could have these return NaN; for now just fix infinite recursion
    for f in [besselj, bessely, besseli, besselk, hankel1, hankel2, yn, jn]:
        assert f(1, S.NaN) == f(1, S.NaN, evaluate=False)

