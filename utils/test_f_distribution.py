
def test_f_distribution():
    d1 = Symbol("d1", positive=True)
    d2 = Symbol("d2", positive=True)

    X = FDistribution("x", d1, d2)

    assert density(X)(x) == (d2**(d2/2)*sqrt((d1*x)**d1*(d1*x + d2)**(-d1 - d2))
                             /(x*beta(d1/2, d2/2)))

    raises(NotImplementedError, lambda: moment_generating_function(X))
    d1 = Symbol("d1", nonpositive=True)
    raises(ValueError, lambda: FDistribution('x', d1, d1))

    d1 = Symbol("d1", positive=True, integer=False)
    raises(ValueError, lambda: FDistribution('x', d1, d1))

    d1 = Symbol("d1", positive=True)
    d2 = Symbol("d2", nonpositive=True)
    raises(ValueError, lambda: FDistribution('x', d1, d2))

    d2 = Symbol("d2", positive=True, integer=False)
    raises(ValueError, lambda: FDistribution('x', d1, d2))

