
def test_bisect_special_parameter(method):
    # give some zeros method strange parameters
    # and check whether an exception appears
    root = 0.1
    args = (1e-09, 0.004, 10, 0.27456)
    rtolbad = 4 * np.finfo(float).eps / 2

    def f(x):
        return x - root

    with pytest.raises(ValueError, match="xtol too small"):
       method(f, -1e8, 1e7, args=args, xtol=-1e-6, rtol=TOL)
    with pytest.raises(ValueError, match="rtol too small"):
       method(f, -1e8, 1e7, args=args, xtol=1e-6, rtol=rtolbad)

