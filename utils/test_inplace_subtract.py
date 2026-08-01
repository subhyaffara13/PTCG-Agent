
def test_inplace_subtract(a, b):
    expected = a - b
    assert m.inplace_subtract(a, b) == expected

