
def test_Frac_preprocess():
    assert Frac.preprocess(False) is False
    assert Frac.preprocess(True) is True

    assert Frac.preprocess(0) is False
    assert Frac.preprocess(1) is True

    raises(OptionError, lambda: Frac.preprocess(x))

