
def test_piecewise_free_symbols():
    f = Piecewise((x, a < 0), (y, True))
    assert f.free_symbols == {x, y, a}

