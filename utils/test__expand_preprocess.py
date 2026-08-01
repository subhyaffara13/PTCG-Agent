
def test_Expand_preprocess():
    assert Expand.preprocess(False) is False
    assert Expand.preprocess(True) is True

    assert Expand.preprocess(0) is False
    assert Expand.preprocess(1) is True

    raises(OptionError, lambda: Expand.preprocess(x))

