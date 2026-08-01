
def test_burr12_ppf_small_arg():
    prob = 1e-16
    quantile = stats.burr12.ppf(prob, 2, 3)
    # The expected quantile was computed using mpmath:
    #   >>> import mpmath
    #   >>> mpmath.mp.dps = 100
    #   >>> prob = mpmath.mpf('1e-16')
    #   >>> c = mpmath.mpf(2)
    #   >>> d = mpmath.mpf(3)
    #   >>> float(((1-prob)**(-1/d) - 1)**(1/c))
    #   5.7735026918962575e-09
    assert_allclose(quantile, 5.7735026918962575e-09)

