
def test_Auto_preprocess():
    assert Auto.preprocess(False) is False
    assert Auto.preprocess(True) is True

    assert Auto.preprocess(0) is False
    assert Auto.preprocess(1) is True

    raises(OptionError, lambda: Auto.preprocess(x))

