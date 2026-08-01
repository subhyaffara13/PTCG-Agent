
def test_issue_18751():
    r = Symbol('r', positive=True)
    theta = Symbol('theta', real=True)
    f = y(n) - 2 * r * cos(theta) * y(n - 1) + r**2 * y(n - 2)
    assert rsolve(f, y(n)) == \
        C0*(r*(cos(theta) - I*Abs(sin(theta))))**n + C1*(r*(cos(theta) + I*Abs(sin(theta))))**n

