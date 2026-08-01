
def test_issue_4737():
    assert integrate(sin(x)/x, (x, -oo, oo)) == pi
    assert integrate(sin(x)/x, (x, 0, oo)) == pi/2
    assert integrate(sin(x)/x, x) == Si(x)

