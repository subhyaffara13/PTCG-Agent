
def test_thread_last():
    assert list(thread_last([1, 2, 3], (map, inc), (filter, iseven))) == [2, 4]
    assert list(thread_last([1, 2, 3], (map, inc), (filter, isodd))) == [3]
    assert thread_last(2, (add, 5), double) == 14

