
def test_issue_3906():
    raises(TypeError, lambda: ask(Q.positive))

