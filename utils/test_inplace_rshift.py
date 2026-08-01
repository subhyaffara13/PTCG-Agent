
def test_inplace_rshift(a, b):
    expected = a >> b
    assert m.inplace_rshift(a, b) == expected

