
def test_issue_5197():
    x = Symbol('x', real=True)
    assert solve(x**2 + 1, x) == []
    n = Symbol('n', integer=True, positive=True)
    assert solve((n - 1)*(n + 2)*(2*n - 1), n) == [1]
    x = Symbol('x', positive=True)
    y = Symbol('y')
    assert solve([x + 5*y - 2, -3*x + 6*y - 15], x, y) == []
                 # not {x: -3, y: 1} b/c x is positive
    # The solution following should not contain (-sqrt(2), sqrt(2))
    assert solve([(x + y), 2 - y**2], x, y) == [(sqrt(2), -sqrt(2))]
    y = Symbol('y', positive=True)
    # The solution following should not contain {y: -x*exp(x/2)}
    assert solve(x**2 - y**2/exp(x), y, x, dict=True) == [{y: x*exp(x/2)}]
    x, y, z = symbols('x y z', positive=True)
    assert solve(z**2*x**2 - z**2*y**2/exp(x), y, x, z, dict=True) == [{y: x*exp(x/2)}]

