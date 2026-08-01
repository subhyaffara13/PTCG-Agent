
def test_issue_3503():
    e = sin(2 + x)/(2 + x)
    assert e.nseries(x, n=2) == sin(2)/2 + x*cos(2)/2 - x*sin(2)/4 + O(x**2)

