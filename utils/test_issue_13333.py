
def test_issue_13333():
    eq = 1/x
    assert eq.subs({"x": '1/2'}) == 2
    assert eq.subs({"x": '(1/2)'}) == 2

