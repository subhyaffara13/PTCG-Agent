
def test_issue_3218():
    assert sympify("x+\ny") == x + y

