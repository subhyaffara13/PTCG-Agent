
def test_Symmetric_preprocess():
    assert Symmetric.preprocess(False) is False
    assert Symmetric.preprocess(True) is True

    assert Symmetric.preprocess(0) is False
    assert Symmetric.preprocess(1) is True

    raises(OptionError, lambda: Symmetric.preprocess(x))

