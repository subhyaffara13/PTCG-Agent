
def test_issue_3639():
    assert sin(cos(x)).nseries(x, n=5) == \
        sin(1) - x**2*cos(1)/2 - x**4*sin(1)/8 + x**4*cos(1)/24 + O(x**5)

