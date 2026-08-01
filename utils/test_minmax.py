
def test_minmax():
    assert mcode(Max(x, y) + Min(x, y)) == "max(x, y) + min(x, y)"
    assert mcode(Max(x, y, z)) == "max(x, max(y, z))"
    assert mcode(Min(x, y, z)) == "min(x, min(y, z))"

