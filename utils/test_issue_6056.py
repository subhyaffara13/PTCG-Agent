
def test_issue_6056():
    assert solve(tanh(x + 3)*tanh(x - 3) - 1) == []
    assert solve(tanh(x - 1)*tanh(x + 1) + 1) == \
            [I*pi*Rational(-3, 4), -I*pi/4, I*pi/4, I*pi*Rational(3, 4)]
    assert solve((tanh(x + 3)*tanh(x - 3) + 1)**2) == \
            [I*pi*Rational(-3, 4), -I*pi/4, I*pi/4, I*pi*Rational(3, 4)]

