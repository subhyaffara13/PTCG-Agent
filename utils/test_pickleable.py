
def test_pickleable():
    # this tests that the _PrintFunction instance is pickleable
    import pickle
    assert pickle.loads(pickle.dumps(latex)) is latex

