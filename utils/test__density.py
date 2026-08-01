
def test_Density():
    X = Die('X', 6)
    d = Density(X)
    assert d.doit() == density(X)

