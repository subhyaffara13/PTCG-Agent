
def test_long_precomputed_cdf():
    x = symbols("x", real=True)
    distribs = [
            Arcsin("A", -5, 9),
            Dagum("D", 4, 10, 3),
            Erlang("E", 14, 5),
            Frechet("F", 2, 6, -3),
            Gamma("G", 2, 7),
            GammaInverse("GI", 3, 5),
            Kumaraswamy("K", 6, 8),
            Laplace("LA", -5, 4),
            Logistic("L", -6, 7),
            Nakagami("N", 2, 7),
            StudentT("S", 4)
            ]
    for distr in distribs:
        for _ in range(5):
            assert tn(diff(cdf(distr)(x), x), density(distr)(x), x, a=0, b=0, c=1, d=0)

    US = UniformSum("US", 5)
    pdf01 = density(US)(x).subs(floor(x), 0).doit()   # pdf on (0, 1)
    cdf01 = cdf(US, evaluate=False)(x).subs(floor(x), 0).doit()   # cdf on (0, 1)
    assert tn(diff(cdf01, x), pdf01, x, a=0, b=0, c=1, d=0)

