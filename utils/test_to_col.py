
def test_to_col():
    c = [1, 2, 3, 4]
    m = to_col(c)
    assert m.domain.is_ZZ
    assert m.shape == (4, 1)
    assert m.flat() == c

