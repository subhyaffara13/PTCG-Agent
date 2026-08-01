
def test_sliding_window_of_short_iterator():
    assert list(sliding_window(3, [1, 2])) == []
    assert list(sliding_window(7, [1, 2])) == []

