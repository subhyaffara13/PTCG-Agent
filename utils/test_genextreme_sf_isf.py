
def test_genextreme_sf_isf():
    # Expected values were computed using mpmath:
    #
    #    import mpmath
    #
    #    def mp_genextreme_sf(x, xi, mu=0, sigma=1):
    #        # Formula from wikipedia, which has a sign convention for xi that
    #        # is the opposite of scipy's shape parameter.
    #        if xi != 0:
    #            t = mpmath.power(1 + ((x - mu)/sigma)*xi, -1/xi)
    #        else:
    #            t = mpmath.exp(-(x - mu)/sigma)
    #        return 1 - mpmath.exp(-t)
    #
    # >>> mpmath.mp.dps = 1000
    # >>> s = mp_genextreme_sf(mpmath.mp.mpf("1e8"), mpmath.mp.mpf("0.125"))
    # >>> float(s)
    # 1.6777205262585625e-57
    # >>> s = mp_genextreme_sf(mpmath.mp.mpf("7.98"), mpmath.mp.mpf("-0.125"))
    # >>> float(s)
    # 1.52587890625e-21
    # >>> s = mp_genextreme_sf(mpmath.mp.mpf("7.98"), mpmath.mp.mpf("0"))
    # >>> float(s)
    # 0.00034218086528426593

    x = 1e8
    s = stats.genextreme.sf(x, -0.125)
    assert_allclose(s, 1.6777205262585625e-57)
    x2 = stats.genextreme.isf(s, -0.125)
    assert_allclose(x2, x)

    x = 7.98
    s = stats.genextreme.sf(x, 0.125)
    assert_allclose(s, 1.52587890625e-21)
    x2 = stats.genextreme.isf(s, 0.125)
    assert_allclose(x2, x)

    x = 7.98
    s = stats.genextreme.sf(x, 0)
    assert_allclose(s, 0.00034218086528426593)
    x2 = stats.genextreme.isf(s, 0)
    assert_allclose(x2, x)

