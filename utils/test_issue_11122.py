
def test_issue_11122():
    x = Symbol('x', extended_positive=False)
    assert unchanged(Gt, x, 0)  # (x > 0)
    # (x > 0) should remain unevaluated after PR #16956

    x = Symbol('x', positive=False, real=True)
    assert (x > 0) is S.false

