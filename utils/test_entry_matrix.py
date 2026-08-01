
def test_entry_matrix():
    X = ImmutableMatrix([[1, 2], [3, 4]])
    assert MatPow(X, 0)[0, 0] == 1
    assert MatPow(X, 0)[0, 1] == 0
    assert MatPow(X, 1)[0, 0] == 1
    assert MatPow(X, 1)[0, 1] == 2
    assert MatPow(X, 2)[0, 0] == 7

