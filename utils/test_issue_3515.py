
def test_issue_3515():
    e = sin(8*x)/x
    assert e.nseries(x, n=6) == 8 - 256*x**2/3 + 4096*x**4/15 + O(x**6)

