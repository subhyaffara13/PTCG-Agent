
def test_trigsimp_issue_7761():
    assert trigsimp(cosh(pi/4)) == cosh(pi/4)

