
def test_dunder_setitem(d, Asp):
    Asp[(1, 1)] = 5
    d[(1, 1)] = 5
    assert d.items() == Asp.items()

