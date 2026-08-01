
def test_issue_15731():
    # f(x)**g(x)=c
    assert solve(Eq((x**2 - 7*x + 11)**(x**2 - 13*x + 42), 1)) == [2, 3, 4, 5, 6, 7]
    assert solve((x)**(x + 4) - 4) == [-2]
    assert solve((-x)**(-x + 4) - 4) == [2]
    assert solve((x**2 - 6)**(x**2 - 2) - 4) == [-2, 2]
    assert solve((x**2 - 2*x - 1)**(x**2 - 3) - 1/(1 - 2*sqrt(2))) == [sqrt(2)]
    assert solve(x**(x + S.Half) - 4*sqrt(2)) == [S(2)]
    assert solve((x**2 + 1)**x - 25) == [2]
    assert solve(x**(2/x) - 2) == [2, 4]
    assert solve((x/2)**(2/x) - sqrt(2)) == [4, 8]
    assert solve(x**(x + S.Half) - Rational(9, 4)) == [Rational(3, 2)]
    # a**g(x)=c
    assert solve((-sqrt(sqrt(2)))**x - 2) == [4, log(2)/(log(2**Rational(1, 4)) + I*pi)]
    assert solve((sqrt(2))**x - sqrt(sqrt(2))) == [S.Half]
    assert solve((-sqrt(2))**x + 2*(sqrt(2))) == [3,
            (3*log(2)**2 + 4*pi**2 - 4*I*pi*log(2))/(log(2)**2 + 4*pi**2)]
    assert solve((sqrt(2))**x - 2*(sqrt(2))) == [3]
    assert solve(I**x + 1) == [2]
    assert solve((1 + I)**x - 2*I) == [2]
    assert solve((sqrt(2) + sqrt(3))**x - (2*sqrt(6) + 5)**Rational(1, 3)) == [Rational(2, 3)]
    # bases of both sides are equal
    b = Symbol('b')
    assert solve(b**x - b**2, x) == [2]
    assert solve(b**x - 1/b, x) == [-1]
    assert solve(b**x - b, x) == [1]
    b = Symbol('b', positive=True)
    assert solve(b**x - b**2, x) == [2]
    assert solve(b**x - 1/b, x) == [-1]

