
def test_issue_10156():
    cx = Sum(2*y**2*x, (x, 1,3))
    e = 2*y*Sum(2*cx*x**2, (x, 1, 9))
    assert e.factor() == \
        8*y**3*Sum(x, (x, 1, 3))*Sum(x**2, (x, 1, 9))

