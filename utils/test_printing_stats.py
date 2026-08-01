
def test_printing_stats():
    # issue 24132
    x = RandomSymbol("x")
    y = RandomSymbol("y")
    z1 = Probability(x > 0)*Identity(2)
    z2 = Expectation(x)*Identity(2)
    z3 = Variance(x)*Identity(2)
    z4 = Covariance(x, y) * Identity(2)

    assert str(z1) == "Probability(x > 0)*I"
    assert str(z2) == "Expectation(x)*I"
    assert str(z3) == "Variance(x)*I"
    assert str(z4) ==  "Covariance(x, y)*I"
    assert z1.is_commutative == False
    assert z2.is_commutative == False
    assert z3.is_commutative == False
    assert z4.is_commutative == False
    assert z2._eval_is_commutative() == False
    assert z3._eval_is_commutative() == False
    assert z4._eval_is_commutative() == False

