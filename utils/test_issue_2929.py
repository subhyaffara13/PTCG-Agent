
def test_issue_2929():
    assert limit((x * exp(x))/(exp(x) - 1), x, -oo) == 0

