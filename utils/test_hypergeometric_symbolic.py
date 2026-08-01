
def test_hypergeometric_symbolic():
    N, m, n = symbols('N, m, n')
    H = Hypergeometric('H', N, m, n)
    dens = density(H).dict
    expec = E(H > 2)
    assert dens == Density(HypergeometricDistribution(N, m, n))
    assert dens.subs(N, 5).doit() == Density(HypergeometricDistribution(5, m, n))
    assert set(dens.subs({N: 3, m: 2, n: 1}).doit().keys()) == {S.Zero, S.One}
    assert set(dens.subs({N: 3, m: 2, n: 1}).doit().values()) == {Rational(1, 3), Rational(2, 3)}
    k = Dummy('k', integer=True)
    assert expec.dummy_eq(
        Sum(Piecewise((k*binomial(m, k)*binomial(N - m, -k + n)
        /binomial(N, n), k > 2), (0, True)), (k, 0, n)))

