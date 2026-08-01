
def test_issue_13297():
    assert manualintegrate(sin(x) * cos(x)**5, x) == -cos(x)**6 / 6

