
def test_klein_gordon_lagrangian():
    m = Symbol('m')
    phi = f(x, t)

    L = -(diff(phi, t)**2 - diff(phi, x)**2 - m**2*phi**2)/2
    eqna = Eq(
        diff(L, phi) - diff(L, diff(phi, x), x) - diff(L, diff(phi, t), t), 0)
    eqnb = Eq(diff(phi, t, t) - diff(phi, x, x) + m**2*phi, 0)
    assert eqna == eqnb

