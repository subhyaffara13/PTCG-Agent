
def test_issue_4945():
    from sympy.abc import H
    assert (H/0).evalf(subs={H:1}) == zoo

