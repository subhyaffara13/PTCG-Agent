
def test_sho_lagrangian():
    m = Symbol('m')
    k = Symbol('k')
    x = f(t)

    L = m*diff(x, t)**2/2 - k*x**2/2
    eqna = Eq(diff(L, x), diff(L, diff(x, t), t))
    eqnb = Eq(-k*x, m*diff(x, t, t))
    assert eqna == eqnb

    assert diff(L, x, t) == diff(L, t, x)
    assert diff(L, diff(x, t), t) == m*diff(x, t, 2)
    assert diff(L, t, diff(x, t)) == -k*x + m*diff(x, t, 2)

