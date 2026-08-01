
def test_FiniteSet_prob():
    E = Exponential('E', 3)
    N = Normal('N', 5, 7)
    assert P(Eq(E, 1)) is S.Zero
    assert P(Eq(N, 2)) is S.Zero
    assert P(Eq(N, x)) is S.Zero

