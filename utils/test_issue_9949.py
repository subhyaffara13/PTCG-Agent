
def test_issue_9949():
    assert is_cnf(to_cnf((b > -5) | (a > 2) & (a < 4)))

