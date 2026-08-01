
def test_inplace_multiply(a, b):
    expected = a * b
    assert m.inplace_multiply(a, b) == expected

