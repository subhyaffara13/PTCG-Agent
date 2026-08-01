
def test_issue_6364():
    a = Symbol('a')
    e = z/(1 - sqrt(1 + z)*sin(a)**2 - sqrt(1 - z)*cos(a)**2)
    assert limit(e, z, 0) == 1/(cos(a)**2 - S.Half)

