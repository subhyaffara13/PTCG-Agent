
def test_issue_6853():
    p = Function('Pi')
    assert latex(p(x)) == r"\Pi{\left(x \right)}"

