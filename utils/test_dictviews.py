
def test_dictviews():
    x = {'a': 1}
    assert dill.copy(x.keys())
    assert dill.copy(x.values())
    assert dill.copy(x.items())

