
def test_rich_cmp():
    assert (x < y) == Lt(x, y)
    assert (x <= y) == Le(x, y)
    assert (x > y) == Gt(x, y)
    assert (x >= y) == Ge(x, y)

