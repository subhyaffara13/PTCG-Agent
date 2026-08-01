
def test_issue_14574():
    assert limit(sqrt(x)*cos(x - x**2) / (x + 1), x, oo) == 0

