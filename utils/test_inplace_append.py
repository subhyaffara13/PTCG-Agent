
def test_inplace_append(a, b):
    expected = a + b
    assert m.inplace_append(a, b) == expected

