
def test_issue_16708():
    m, vi = symbols('m vi', positive=True)
    B, ti, d = symbols('B ti d')
    assert limit((B*ti*vi - sqrt(m)*sqrt(-2*B*d*vi + m*(vi)**2) + m*vi)/(B*vi), B, 0) == (d + ti*vi)/vi

