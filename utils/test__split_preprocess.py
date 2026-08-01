
def test_Split_preprocess():
    assert Split.preprocess(False) is False
    assert Split.preprocess(True) is True

    assert Split.preprocess(0) is False
    assert Split.preprocess(1) is True

    raises(OptionError, lambda: Split.preprocess(x))

