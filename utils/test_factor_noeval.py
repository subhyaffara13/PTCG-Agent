
def test_factor_noeval():
    assert factor(6*x - 10) == Mul(2, 3*x - 5, evaluate=False)
    assert factor((6*x - 10)/(3*x - 6)) == Mul(Rational(2, 3), 3*x - 5, 1/(x - 2))

