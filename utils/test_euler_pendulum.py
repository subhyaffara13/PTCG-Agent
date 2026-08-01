
def test_euler_pendulum():
    x = Function('x')
    t = Symbol('t')
    L = D(x(t), t)**2/2 + cos(x(t))
    assert euler(L, x(t), t) == [Eq(-sin(x(t)) - D(x(t), t, t), 0)]

