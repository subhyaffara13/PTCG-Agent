
def test_issue_20389():
    result = degree(x * (x + 1) - x ** 2 - x, x)
    assert result == -oo

