
def test_issue_22757():
    assert manualintegrate(sin(x), y) == y * sin(x)

