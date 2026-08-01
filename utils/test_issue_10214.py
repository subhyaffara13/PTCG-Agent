
def test_issue_10214():
    assert solveset(x**Rational(3, 2) + 4, x, S.Reals) == S.EmptySet
    assert solveset(x**(Rational(-3, 2)) + 4, x, S.Reals) == S.EmptySet

    ans = FiniteSet(-2**Rational(2, 3))
    assert solveset(x**(S(3)) + 4, x, S.Reals) == ans
    assert (x**(S(3)) + 4).subs(x,list(ans)[0]) == 0 # substituting ans and verifying the result.
    assert (x**(S(3)) + 4).subs(x,-(-2)**Rational(2, 3)) == 0

