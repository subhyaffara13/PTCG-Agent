
def test_sorted():
    assert sorted(key=second)([(1, 2), (2, 1)]) == [(2, 1), (1, 2)]

