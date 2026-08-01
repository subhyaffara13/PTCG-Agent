
def test_base_ordering():
    base = [2, 4, 5]
    degree = 7
    assert _base_ordering(base, degree) == [3, 4, 0, 5, 1, 2, 6]

