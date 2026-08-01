
def test_Polys_preprocess():
    assert Polys.preprocess(False) is False
    assert Polys.preprocess(True) is True

    assert Polys.preprocess(0) is False
    assert Polys.preprocess(1) is True

    raises(OptionError, lambda: Polys.preprocess(x))

