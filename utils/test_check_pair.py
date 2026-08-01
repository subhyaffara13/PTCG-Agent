
def test_check_pair():
    assert _check_pair([0, 1, 0], [0, 1, 1]) == 2
    assert _check_pair([0, 1, 0], [1, 1, 1]) == -1

