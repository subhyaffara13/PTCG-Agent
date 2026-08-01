
def test_rsolve_raises():
    x = Function('x')
    raises(ValueError, lambda: rsolve(y(n) - y(k + 1), y(n)))
    raises(ValueError, lambda: rsolve(y(n) - y(n + 1), x(n)))
    raises(ValueError, lambda: rsolve(y(n) - x(n + 1), y(n)))
    raises(ValueError, lambda: rsolve(y(n) - sqrt(n)*y(n + 1), y(n)))
    raises(ValueError, lambda: rsolve(y(n) - y(n + 1), y(n), {x(0): 0}))
    raises(ValueError, lambda: rsolve(y(n) + y(n + 1) + 2**n + cos(n), y(n)))

