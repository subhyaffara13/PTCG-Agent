
def test_issue_3258():
    a = x/(exp(x) - 1)
    assert a.nseries(x, 0, 5) == 1 - x/2 - x**4/720 + x**2/12 + O(x**5)

