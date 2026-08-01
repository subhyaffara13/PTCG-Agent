
def test_EX_ordering():
    elements = [EX(1), EX(x), EX(3)]
    assert sorted(elements) == [EX(1), EX(3), EX(x)]

