
def test_conditional_eq():
    E = Exponential('E', 1)
    assert P(Eq(E, 1), Eq(E, 1)) == 1
    assert P(Eq(E, 1), Eq(E, 2)) == 0
    assert P(E > 1, Eq(E, 2)) == 1
    assert P(E < 1, Eq(E, 2)) == 0

