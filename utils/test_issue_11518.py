
def test_issue_11518():
    x = Symbol("x", real=True)
    y = Symbol("y", real=True)
    r = sqrt(x**2 + y**2)
    assert conjugate(r) == r
    s = abs(x + I * y)
    assert conjugate(s) == r

