
def test_inplace_and(a, b):
    expected = a & b
    assert m.inplace_and(a, b) == expected

