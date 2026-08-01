
def test_weibull_min_sas1():
    # Data and SAS results from
    #   https://support.sas.com/documentation/cdl/en/qcug/63922/HTML/default/
    #         viewer.htm#qcug_reliability_sect004.htm

    text = """
           450 0    460 1   1150 0   1150 0   1560 1
          1600 0   1660 1   1850 1   1850 1   1850 1
          1850 1   1850 1   2030 1   2030 1   2030 1
          2070 0   2070 0   2080 0   2200 1   3000 1
          3000 1   3000 1   3000 1   3100 0   3200 1
          3450 0   3750 1   3750 1   4150 1   4150 1
          4150 1   4150 1   4300 1   4300 1   4300 1
          4300 1   4600 0   4850 1   4850 1   4850 1
          4850 1   5000 1   5000 1   5000 1   6100 1
          6100 0   6100 1   6100 1   6300 1   6450 1
          6450 1   6700 1   7450 1   7800 1   7800 1
          8100 1   8100 1   8200 1   8500 1   8500 1
          8500 1   8750 1   8750 0   8750 1   9400 1
          9900 1  10100 1  10100 1  10100 1  11500 1
    """

    life, cens = np.array([int(w) for w in text.split()]).reshape(-1, 2).T
    life = life/1000.0

    data = CensoredData.right_censored(life, cens)

    c, loc, scale = weibull_min.fit(data, floc=0, optimizer=optimizer)
    assert_allclose(c, 1.0584, rtol=1e-4)
    assert_allclose(scale, 26.2968, rtol=1e-5)
    assert loc == 0

