
def test_issue_8235():
    assert reduce_inequalities(x**2 - 1 < 0) == \
        And(S.NegativeOne < x, x < 1)
    assert reduce_inequalities(x**2 - 1 <= 0) == \
        And(S.NegativeOne <= x, x <= 1)
    assert reduce_inequalities(x**2 - 1 > 0) == \
        Or(And(-oo < x, x < -1), And(x < oo, S.One < x))
    assert reduce_inequalities(x**2 - 1 >= 0) == \
        Or(And(-oo < x, x <= -1), And(S.One <= x, x < oo))

    eq = x**8 + x - 9  # we want CRootOf solns here
    sol = solve(eq >= 0)
    tru = Or(And(rootof(eq, 1) <= x, x < oo), And(-oo < x, x <= rootof(eq, 0)))
    assert sol == tru

    # recast vanilla as real
    assert solve(sqrt((-x + 1)**2) < 1) == And(S.Zero < x, x < 2)

