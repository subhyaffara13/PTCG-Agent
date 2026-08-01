
def test_issue_5421():
    raises(TypeError, lambda: ask(pi/log(x), Q.real))

