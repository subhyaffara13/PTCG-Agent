
def test_gammaincc():
    # Check that the gammaincc in special._precompute.gammainc_data
    # agrees with mpmath's gammainc.
    assert_mpmath_equal(lambda a, x: gammaincc(a, x, dps=1000),
                        lambda a, x: mp.gammainc(a, a=x, regularized=True),
                        [Arg(20, 100), Arg(20, 100)],
                        nan_ok=False, rtol=1e-17, n=50, dps=1000)

    # Test the fast integer path
    assert_mpmath_equal(gammaincc,
                        lambda a, x: mp.gammainc(a, a=x, regularized=True),
                        [IntArg(1, 100), Arg(0, 100)],
                        nan_ok=False, rtol=1e-17, n=50, dps=50)

