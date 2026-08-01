
def test_at(arr):
    assert m.at_t(arr, 0, 2) == 3
    assert m.at_t(arr, 1, 0) == 4

    assert all(m.mutate_at_t(arr, 0, 2).ravel() == [1, 2, 4, 4, 5, 6])
    assert all(m.mutate_at_t(arr, 1, 0).ravel() == [1, 2, 4, 5, 5, 6])

