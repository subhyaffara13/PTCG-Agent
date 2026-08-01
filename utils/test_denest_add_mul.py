
def test_denest_add_mul():
    # when working with evaluated expressions make sure they denest
    eq = x + 1
    eq = Add(eq, 2, evaluate=False)
    eq = Add(eq, 2, evaluate=False)
    assert Add(*eq.args) == x + 5
    eq = x*2
    eq = Mul(eq, 2, evaluate=False)
    eq = Mul(eq, 2, evaluate=False)
    assert Mul(*eq.args) == 8*x
    # but don't let them denest unnecessarily
    eq = Mul(-2, x - 2, evaluate=False)
    assert 2*eq == Mul(-4, x - 2, evaluate=False)
    assert -eq == Mul(2, x - 2, evaluate=False)

