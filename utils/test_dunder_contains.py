
def test_dunder_contains(d, Asp):
    assert ((0, 1) in d) == ((0, 1) in Asp)
    assert ((0, 0) in d) == ((0, 0) in Asp)

