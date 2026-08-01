
def test_issue_10195():
    a = Symbol('a', integer=True)
    l = Symbol('l', even=True, nonzero=True)
    n = Symbol('n', odd=True)
    e_x = (-1)**(n/2 - S.Half) - (-1)**(n*Rational(3, 2) - S.Half)
    assert powsimp((-1)**(l/2)) == I**l
    assert powsimp((-1)**(n/2)) == I**n
    assert powsimp((-1)**(n*Rational(3, 2))) == -I**n
    assert powsimp(e_x) == (-1)**(n/2 - S.Half) + (-1)**(n*Rational(3, 2) +
            S.Half)
    assert powsimp((-1)**(a*Rational(3, 2))) == (-I)**a

