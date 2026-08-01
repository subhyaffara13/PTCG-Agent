
def test_issue_8170():
    assert integrate(tan(x), (x, 0, pi/2)) is S.Infinity

