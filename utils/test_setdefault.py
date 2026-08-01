
def test_setdefault(d, Asp):
    assert Asp.setdefault((0, 1), 4) == 1
    assert Asp.setdefault((2, 2), 4) == 4
    d.setdefault((0, 1), 4)
    d.setdefault((2, 2), 4)
    assert d.items() == Asp.items()

