
def test_Formal_preprocess():
    assert Formal.preprocess(False) is False
    assert Formal.preprocess(True) is True

    assert Formal.preprocess(0) is False
    assert Formal.preprocess(1) is True

    raises(OptionError, lambda: Formal.preprocess(x))

