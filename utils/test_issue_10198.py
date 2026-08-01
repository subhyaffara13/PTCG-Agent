
def test_issue_10198():
    assert reduce_inequalities(
        -1 + 1/abs(1/x - 1) < 0) == (x > -oo) & (x < S(1)/2) & Ne(x, 0)

    assert reduce_inequalities(abs(1/sqrt(x)) - 1, x) == Eq(x, 1)
    assert reduce_abs_inequality(-3 + 1/abs(1 - 1/x), '<', x) == \
        Or(And(-oo < x, x < 0),
        And(S.Zero < x, x < Rational(3, 4)), And(Rational(3, 2) < x, x < oo))
    raises(ValueError,lambda: reduce_abs_inequality(-3 + 1/abs(
        1 - 1/sqrt(x)), '<', x))

