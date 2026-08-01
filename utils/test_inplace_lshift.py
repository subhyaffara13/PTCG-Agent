
def test_inplace_lshift(a, b):
    expected = a << b
    assert m.inplace_lshift(a, b) == expected

