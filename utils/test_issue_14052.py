
def test_issue_14052():
    assert integrate(abs(sin(x)), (x, 0, 2*pi)) == 4

