
def test_issue_14096():
    assert integrate(1/(x + y)**2, (x, 0, 1)) == -1/(y + 1) + 1/y
    assert integrate(1/(1 + x + y + z)**2, (x, 0, 1), (y, 0, 1), (z, 0, 1)) == \
        -4*log(4) - 6*log(2) + 9*log(3)

