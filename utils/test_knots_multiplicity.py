
def test_knots_multiplicity():
    # Take a spline w/ random coefficients, throw in knots of varying
    # multiplicity.

    def check_splev(b, j, der=0, atol=1e-14, rtol=1e-14):
        # check evaluations against FITPACK, incl extrapolations
        t, c, k = b.tck
        x = np.unique(t)
        x = np.r_[t[0]-0.1, 0.5*(x[1:] + x[:1]), t[-1]+0.1]
        xp_assert_close(splev(x, (t, c, k), der), b(x, der),
                atol=atol, rtol=rtol, err_msg=f'der = {der}  k = {b.k}')

    # test loop itself
    # [the index `j` is for interpreting the traceback in case of a failure]
    for k in [1, 2, 3, 4, 5]:
        b = _make_random_spline(k=k)
        for j, b1 in enumerate(_make_multiples(b)):
            check_splev(b1, j)
            for der in range(1, k+1):
                check_splev(b1, j, der, 1e-12, 1e-12)

