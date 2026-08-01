
def test_issue_17524():
    a = symbols("a", real=True)
    e = (-1 - a**2)*sqrt(1 + a**2)
    assert signsimp(powsimp(e)) == signsimp(e) == -(a**2 + 1)**(S(3)/2)

