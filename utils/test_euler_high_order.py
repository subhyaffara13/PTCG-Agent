
def test_euler_high_order():
    # an example from hep-th/0309038
    m = Symbol('m')
    k = Symbol('k')
    x = Function('x')
    y = Function('y')
    t = Symbol('t')
    L = (m*D(x(t), t)**2/2 + m*D(y(t), t)**2/2 -
         k*D(x(t), t)*D(y(t), t, t) + k*D(y(t), t)*D(x(t), t, t))
    assert euler(L, [x(t), y(t)]) == [Eq(2*k*D(y(t), t, t, t) -
                                         m*D(x(t), t, t), 0),
                                      Eq(-2*k*D(x(t), t, t, t) -
                                         m*D(y(t), t, t), 0)]

    w = Symbol('w')
    L = D(x(t, w), t, w)**2/2
    assert euler(L) == [Eq(D(x(t, w), t, t, w, w), 0)]

