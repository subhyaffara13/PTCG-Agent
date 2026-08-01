
def test_todense(A):
    assert not isinstance(A.todense(), np.matrix), \
        "Expected array, got matrix"

