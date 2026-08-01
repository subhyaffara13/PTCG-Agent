
def test_nan_inequality_raise_errors():
    # See discussion in pull request #7776.  We test inequalities with
    # a set including examples of various classes.
    for q in (x, S.Zero, S(10), S.One/3, pi, S(1.3), oo, -oo, nan):
        assert_all_ineq_raise_TypeError(q, nan)

