
def test_small_tolerances_for_lm():
    for ftol, xtol, gtol in [(None, 1e-13, 1e-13),
                             (1e-13, None, 1e-13),
                             (1e-13, 1e-13, None)]:
        assert_raises(ValueError, least_squares, fun_trivial, 2.0, xtol=xtol,
                      ftol=ftol, gtol=gtol, method='lm')

