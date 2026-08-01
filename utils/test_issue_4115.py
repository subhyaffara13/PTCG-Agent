
def test_issue_4115():
    assert (sin(x)/(1 - cos(x))).nseries(x, n=1) == 2/x + O(x)
    assert (sin(x)**2/(1 - cos(x))).nseries(x, n=1) == 2 + O(x)

