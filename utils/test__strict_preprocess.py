
def test_Strict_preprocess():
    assert Strict.preprocess(False) is False
    assert Strict.preprocess(True) is True

    assert Strict.preprocess(0) is False
    assert Strict.preprocess(1) is True

    raises(OptionError, lambda: Strict.preprocess(x))

