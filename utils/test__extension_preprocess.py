
def test_Extension_preprocess():
    assert Extension.preprocess(True) is True
    assert Extension.preprocess(1) is True

    assert Extension.preprocess([]) is None

    assert Extension.preprocess(sqrt(2)) == {sqrt(2)}
    assert Extension.preprocess([sqrt(2)]) == {sqrt(2)}

    assert Extension.preprocess([sqrt(2), I]) == {sqrt(2), I}

    raises(OptionError, lambda: Extension.preprocess(False))
    raises(OptionError, lambda: Extension.preprocess(0))

