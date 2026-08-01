
def test_issue_4100():
    R = Symbol('R', positive=True)
    assert integrate(sqrt(R**2 - x**2), (x, 0, R)) == pi*R**2/4

