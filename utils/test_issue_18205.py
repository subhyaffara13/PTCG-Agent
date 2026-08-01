
def test_issue_18205():
    assert cancel((2 + I)*(3 - I)) == 7 + I
    assert cancel((2 + I)*(2 - I)) == 5

