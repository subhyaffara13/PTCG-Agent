
def test_call():
    a, b, x = symbols('a, b, x', cls=Dummy)
    f = Hyper_Function([2, a], [b])
    assert f(x) == hyper([2, a], [b], x)


def test_call():
    x, y = symbols('x y')
    # See the long history of this in issues 5026 and 5105.

    raises(TypeError, lambda: sin(x)({ x : 1, sin(x) : 2}))
    raises(TypeError, lambda: sin(x)(1))

    # No effect as there are no callables
    assert sin(x).rcall(1) == sin(x)
    assert (1 + sin(x)).rcall(1) == 1 + sin(x)

    # Effect in the presence of callables
    l = Lambda(x, 2*x)
    assert (l + x).rcall(y) == 2*y + x
    assert (x**l).rcall(2) == x**4
    # TODO UndefinedFunction does not subclass Expr
    #f = Function('f')
    #assert (2*f)(x) == 2*f(x)

    assert (Q.real & Q.positive).rcall(x) == Q.real(x) & Q.positive(x)


def test_call(Poly):
    P = Polynomial
    d = Poly.domain
    x = np.linspace(d[0], d[1], 11)

    # Check defaults
    p = Poly.cast(P([1, 2, 3]))
    tgt = 1 + x * (2 + 3 * x)
    res = p(x)
    assert_almost_equal(res, tgt)

