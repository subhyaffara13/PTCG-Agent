
def test_Mul_is_irrational():
    expr = Mul(1, 2, 3, evaluate=False)
    assert expr.is_irrational is False
    expr = Mul(1, I, I, evaluate=False)
    assert expr.is_rational is None # I * I = -1 but *no evaluation allowed*
    # sqrt(2) * I * I = -sqrt(2) is irrational but
    # this can't be determined without evaluating the
    # expression and the eval_is routines shouldn't do that
    expr = Mul(sqrt(2), I, I, evaluate=False)
    assert expr.is_irrational is None

