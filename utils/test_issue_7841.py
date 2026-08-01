
def test_issue_7841():
    raises(TypeError, lambda: x in S.Reals)

