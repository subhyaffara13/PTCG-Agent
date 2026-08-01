
def test_legacy():
    # Legacy behavior: truncating arguments to integers
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", "floating point number truncated to an integer", RuntimeWarning)
        assert_equal(special.expn(1, 0.3), special.expn(1.8, 0.3))
        assert_equal(special.nbdtrc(1, 2, 0.3), special.nbdtrc(1.8, 2.8, 0.3))
        assert_equal(special.nbdtr(1, 2, 0.3), special.nbdtr(1.8, 2.8, 0.3))
        assert_equal(special.nbdtri(1, 2, 0.3), special.nbdtri(1.8, 2.8, 0.3))
        assert_equal(special.pdtri(1, 0.3), special.pdtri(1.8, 0.3))
        assert_equal(special.kn(1, 0.3), special.kn(1.8, 0.3))
        assert_equal(special.yn(1, 0.3), special.yn(1.8, 0.3))
        assert_equal(special.smirnov(1, 0.3), special.smirnov(1.8, 0.3))
        assert_equal(special.smirnovi(1, 0.3), special.smirnovi(1.8, 0.3))

