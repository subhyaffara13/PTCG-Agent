
def test_pro_rad1():
    # https://github.com/scipy/scipy/issues/21058
    # Reference values taken from WolframAlpha
    # SpheroidalS1(1, 1, 30, 1.1)
    # SpheroidalS1Prime(1, 1, 30, 1.1)
    res = special.pro_rad1(1, 1, 30, 1.1)
    assert_allclose(res, (0.009657872296166435, 3.253369651472877), rtol=2e-5)

