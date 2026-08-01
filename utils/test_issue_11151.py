
def test_issue_11151():
    z = S.Zero
    e = Sum(z, (x, 1, 2))
    assert e != z  # it shouldn't evaluate
    # when it does evaluate, this is what it should give
    assert evalf(e, 15, {}) == \
        evalf(z, 15, {}) == (None, None, 15, None)
    # so this shouldn't fail
    assert (e/2).n() == 0
    # this was where the issue appeared
    expr0 = Sum(x**2 + x, (x, 1, 2))
    expr1 = Sum(0, (x, 1, 2))
    expr2 = expr1/expr0
    assert simplify(factor(expr2) - expr2) == 0

