
def test_reduce_inequalities_general():
    assert reduce_inequalities(Ge(sqrt(2)*x, 1)) == And(sqrt(2)/2 <= x, x < oo)
    assert reduce_inequalities(x + 1 > 0) == And(S.NegativeOne < x, x < oo)

