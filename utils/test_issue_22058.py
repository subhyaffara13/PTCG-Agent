
def test_issue_22058():
    sol = solveset(-sqrt(t)*x**2 + 2*x + sqrt(t), x, S.Reals)
    # doesn't fail (and following numerical check)
    assert sol.xreplace({t: 1}) == {1 - sqrt(2), 1 + sqrt(2)}, sol.xreplace({t: 1})

