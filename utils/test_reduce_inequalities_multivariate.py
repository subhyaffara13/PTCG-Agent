
def test_reduce_inequalities_multivariate():
    assert reduce_inequalities([Ge(x**2, 1), Ge(y**2, 1)]) == And(
        Or(And(Le(S.One, x), Lt(x, oo)), And(Le(x, -1), Lt(-oo, x))),
        Or(And(Le(S.One, y), Lt(y, oo)), And(Le(y, -1), Lt(-oo, y))))

