
def test_All_preprocess():
    assert All.preprocess(False) is False
    assert All.preprocess(True) is True

    assert All.preprocess(0) is False
    assert All.preprocess(1) is True

    raises(OptionError, lambda: All.preprocess(x))

