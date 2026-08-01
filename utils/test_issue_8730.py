
def test_issue_8730():
    assert limit(subfactorial(x), x, oo) is oo

