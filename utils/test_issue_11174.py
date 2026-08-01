
def test_issue_11174():
    eq = z**2 + exp(2*x) - sin(y)
    soln = Intersection(S.Reals, FiniteSet(log(-z**2 + sin(y))/2))
    assert solveset(eq, x, S.Reals) == soln

    eq = sqrt(r)*Abs(tan(t))/sqrt(tan(t)**2 + 1) + x*tan(t)
    s = -sqrt(r)*Abs(tan(t))/(sqrt(tan(t)**2 + 1)*tan(t))
    soln = Intersection(S.Reals, FiniteSet(s))
    assert solveset(eq, x, S.Reals) == soln


def test_issue_11174():
    soln = Intersection(Interval(-oo, oo), FiniteSet(-x), evaluate=False)
    assert Intersection(FiniteSet(-x), S.Reals) == soln

    soln = Intersection(S.Reals, FiniteSet(x), evaluate=False)
    assert Intersection(FiniteSet(x), S.Reals) == soln

