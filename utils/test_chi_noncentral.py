
def test_chi_noncentral():
    k = Symbol("k", integer=True)
    l = Symbol("l")

    X = ChiNoncentral("x", k, l)
    assert density(X)(x) == (x**k*l*(x*l)**(-k/2)*
                          exp(-x**2/2 - l**2/2)*besseli(k/2 - 1, x*l))

    k = Symbol("k", integer=True, positive=False)
    raises(ValueError, lambda: ChiNoncentral('x', k, l))

    k = Symbol("k", integer=True, positive=True)
    l = Symbol("l", nonpositive=True)
    raises(ValueError, lambda: ChiNoncentral('x', k, l))

    k = Symbol("k", integer=False)
    l = Symbol("l", positive=True)
    raises(ValueError, lambda: ChiNoncentral('x', k, l))

