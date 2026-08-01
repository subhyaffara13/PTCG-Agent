
def test_pro_rad2():
    # https://github.com/scipy/scipy/issues/21461
    # Reference values taken from WolframAlpha
    # SpheroidalS2(0, 0, 3, 1.02)
    # SpheroidalS2Prime(0, 0, 3, 1.02)
    res = special.pro_rad2(0, 0, 3, 1.02)
    assert_allclose(res, (-0.35089596858528077, 13.652764213480872), rtol=10e-10)

