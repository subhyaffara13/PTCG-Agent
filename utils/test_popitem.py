
def test_popitem(d, Asp):
    assert d.popitem() == Asp.popitem()
    assert d.items() == Asp.items()

