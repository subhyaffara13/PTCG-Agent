
def test_origbases():
    assert dill.copy(customIntList).__orig_bases__ == customIntList.__orig_bases__

