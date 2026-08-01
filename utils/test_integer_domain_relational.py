
def test_integer_domain_relational():
    eq1 = 2*x + 3 > 0
    eq2 = x**2 + 3*x - 2 >= 0
    eq3 = x + 1/x > -2 + 1/x
    eq4 = x + sqrt(x**2 - 5) > 0
    eq = x + 1/x > -2 + 1/x
    eq5 = eq.subs(x,log(x))
    eq6 = log(x)/x <= 0
    eq7 = log(x)/x < 0
    eq8 = x/(x-3) < 3
    eq9 = x/(x**2-3) < 3

    assert solveset(eq1, x, S.Integers) == Range(-1, oo, 1)
    assert solveset(eq2, x, S.Integers) == Union(Range(-oo, -3, 1), Range(1, oo, 1))
    assert solveset(eq3, x, S.Integers) == Union(Range(-1, 0, 1), Range(1, oo, 1))
    assert solveset(eq4, x, S.Integers) == Range(3, oo, 1)
    assert solveset(eq5, x, S.Integers) == Range(2, oo, 1)
    assert solveset(eq6, x, S.Integers) == Range(1, 2, 1)
    assert solveset(eq7, x, S.Integers) == S.EmptySet
    assert solveset(eq8, x, domain=Range(0,5)) == Range(0, 3, 1)
    assert solveset(eq9, x, domain=Range(0,5)) == Union(Range(0, 2, 1), Range(2, 5, 1))

    # test_issue_19794
    assert solveset(x + 2 < 0, x, S.Integers) == Range(-oo, -2, 1)

