
def test_bessel_twoinputs():
    for f in [besselj, bessely, besseli, besselk, hankel1, hankel2, jn, yn]:
        raises(TypeError, lambda: f(1))
        raises(TypeError, lambda: f(1, 2, 3))

