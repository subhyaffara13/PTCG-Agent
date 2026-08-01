
def test_issue_20365():
    assert limit(((x + 1)**(1/x) - E)/x, x, 0) == -E/2

