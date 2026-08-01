
def test_issue_3595():
    assert sympify("a_") == Symbol("a_")
    assert sympify("_a") == Symbol("_a")

