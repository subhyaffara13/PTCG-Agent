
def test_Greedy_preprocess():
    assert Greedy.preprocess(False) is False
    assert Greedy.preprocess(True) is True

    assert Greedy.preprocess(0) is False
    assert Greedy.preprocess(1) is True

    raises(OptionError, lambda: Greedy.preprocess(x))

