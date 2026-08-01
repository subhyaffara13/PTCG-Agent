
def test_issue_21355():
    assert radsimp(1/(x + sqrt(x**2))) == 1/(x + sqrt(x**2))
    assert radsimp(1/(x - sqrt(x**2))) == 1/(x - sqrt(x**2))

