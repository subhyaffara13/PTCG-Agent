
def test_issue_6605():
    x = symbols('x')
    assert solve(4**(x/2) - 2**(x/3)) == [0, 3*I*pi/log(2)]
    # while the first one passed, this one failed
    x = symbols('x', real=True)
    assert solve(5**(x/2) - 2**(x/3)) == [0]
    b = sqrt(6)*sqrt(log(2))/sqrt(log(5))
    assert solve(5**(x/2) - 2**(3/x)) == [-b, b]

