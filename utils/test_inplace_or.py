
def test_inplace_or(a, b):
    expected = a | b
    assert m.inplace_or(a, b) == expected

