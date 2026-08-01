
def test_issue_7322():
    number = 5.62527e-35
    assert solve(x - number, x)[0] == number

