
def test_dunder_delitem(d, Asp):
    del Asp[(0, 1)]
    del d[(0, 1)]
    assert d.items() == Asp.items()

