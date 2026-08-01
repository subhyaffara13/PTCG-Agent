
def test_issue_5414():
    assert ratint(1/(x**2 + 16), x) == atan(x/4)/4

