
def test_Include_preprocess():
    assert Include.preprocess(False) is False
    assert Include.preprocess(True) is True

    assert Include.preprocess(0) is False
    assert Include.preprocess(1) is True

    raises(OptionError, lambda: Include.preprocess(x))

