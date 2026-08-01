
def test_Gaussian_preprocess():
    assert Gaussian.preprocess(False) is False
    assert Gaussian.preprocess(True) is True

    assert Gaussian.preprocess(0) is False
    assert Gaussian.preprocess(1) is True

    raises(OptionError, lambda: Gaussian.preprocess(x))

