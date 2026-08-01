
def test_issue_13112():
    assert integrate(sin(t)**2 / (5 - 4*cos(t)), [t, 0, 2*pi]) == pi / 4

