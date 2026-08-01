
def test_issue_18118():
    assert limit(sign(sin(x)), x, 0, "-") == -1
    assert limit(sign(sin(x)), x, 0, "+") == 1

