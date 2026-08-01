
def test_issue_11534():
    # eq1 and eq2 should not have the same solutions because squaring both
    # sides of the radical equation introduces a spurious solution branch.
    # The equations have a symbolic parameter y and it is easy to see that for
    # y != 0 the solution s1 will not be valid for eq1.
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    eq1 = -y + x/sqrt(-x**2 + 1)
    eq2 = -y**2 + x**2/(-x**2 + 1)

    # We get a ConditionSet here because s1 works in eq1 if y is equal to zero
    # although not for any other value of y. That case is redundant though
    # because if y=0 then s1=s2 so the solution for eq1 could just be returned
    # as s2 - {-1, 1}. In fact we have
    #   |y/sqrt(y**2 + 1)| < 1
    # So the complements are not needed either. The ideal output here would be
    #   sol1 = s2
    #   sol2 = s1 | s2.
    s1, s2 = FiniteSet(-y/sqrt(y**2 + 1)), FiniteSet(y/sqrt(y**2 + 1))
    cset = ConditionSet(x, Eq(eq1, 0), s1)
    sol1 = (s2 - {-1, 1}) | (cset - {-1, 1})
    sol2 = (s1 | s2) - {-1, 1}

    assert solveset(eq1, x, S.Reals) == sol1
    assert solveset(eq2, x, S.Reals) == sol2

