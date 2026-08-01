
def test_mutate_data(arr):
    assert all(m.mutate_data(arr).ravel() == [2, 4, 6, 8, 10, 12])
    assert all(m.mutate_data(arr).ravel() == [4, 8, 12, 16, 20, 24])
    assert all(m.mutate_data(arr, 1).ravel() == [4, 8, 12, 32, 40, 48])
    assert all(m.mutate_data(arr, 0, 1).ravel() == [4, 16, 24, 64, 80, 96])
    assert all(m.mutate_data(arr, 1, 2).ravel() == [4, 16, 24, 64, 80, 192])

    assert all(m.mutate_data_t(arr).ravel() == [5, 17, 25, 65, 81, 193])
    assert all(m.mutate_data_t(arr).ravel() == [6, 18, 26, 66, 82, 194])
    assert all(m.mutate_data_t(arr, 1).ravel() == [6, 18, 26, 67, 83, 195])
    assert all(m.mutate_data_t(arr, 0, 1).ravel() == [6, 19, 27, 68, 84, 196])
    assert all(m.mutate_data_t(arr, 1, 2).ravel() == [6, 19, 27, 68, 84, 197])

