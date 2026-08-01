
def test_issue_15709():
    assert powsimp(3**x*Rational(2, 3)) == 2*3**(x-1)
    assert powsimp(2*3**x/3) == 2*3**(x-1)

