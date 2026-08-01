
def test_issue_6097():
    assert collect(a*y**(2.0*x) + b*y**(2.0*x), y**x) == (a + b)*(y**x)**2.0
    assert collect(a*2**(2.0*x) + b*2**(2.0*x), 2**x) == (a + b)*(2**x)**2.0

