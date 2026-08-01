
def test_beta_noncentral():
    a, b = symbols('a b', positive=True)
    c = Symbol('c', nonnegative=True)
    _k = Dummy('k')

    X = BetaNoncentral('x', a, b, c)

    assert pspace(X).domain.set == Interval(0, 1)

    dens = density(X)
    z = Symbol('z')

    res = Sum( z**(_k + a - 1)*(c/2)**_k*(1 - z)**(b - 1)*exp(-c/2)/
               (beta(_k + a, b)*factorial(_k)), (_k, 0, oo))
    assert dens(z).dummy_eq(res)

    # BetaCentral should not raise if the assumptions
    # on the symbols can not be determined
    a, b, c = symbols('a b c')
    assert BetaNoncentral('x', a, b, c)

    a = Symbol('a', positive=False, real=True)
    raises(ValueError, lambda: BetaNoncentral('x', a, b, c))

    a = Symbol('a', positive=True)
    b = Symbol('b', positive=False, real=True)
    raises(ValueError, lambda: BetaNoncentral('x', a, b, c))

    a = Symbol('a', positive=True)
    b = Symbol('b', positive=True)
    c = Symbol('c', nonnegative=False, real=True)
    raises(ValueError, lambda: BetaNoncentral('x', a, b, c))

