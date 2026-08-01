
def test_prob_neq():
    E = Exponential('E', 4)
    X = ChiSquared('X', 4)
    assert P(Ne(E, 2)) == 1
    assert P(Ne(X, 4)) == 1
    assert P(Ne(X, 4)) == 1
    assert P(Ne(X, 5)) == 1
    assert P(Ne(E, x)) == 1

