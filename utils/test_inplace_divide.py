
def test_inplace_divide(a, b):
    expected = a / b
    assert m.inplace_divide(a, b) == expected

