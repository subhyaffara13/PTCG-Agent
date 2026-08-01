
def test_has_dups():
    assert has_dups(set()) is False
    assert has_dups(list(range(3))) is False
    assert has_dups([1, 2, 1]) is True
    assert has_dups([[1], [1]]) is True
    assert has_dups([[1], [2]]) is False

