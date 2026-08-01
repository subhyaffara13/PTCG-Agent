
def test_arbitrary_element(iterable_type, expected):
    iterable = iterable_type([1, 2, 3])
    assert arbitrary_element(iterable) == expected

