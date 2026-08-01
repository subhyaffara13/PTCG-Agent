
def test_FinitePSpace():
    X = Die('X', 6)
    space = pspace(X)
    assert space.density == DieDistribution(6)

