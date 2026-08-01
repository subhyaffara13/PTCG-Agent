
def test_sample_scipy():
    distribs_scipy = [
        MultivariateNormal("M", [0, 0], [[0.1, 0.025], [0.025, 0.1]]),
        MultivariateBeta("B", [0.4, 5, 15]),
        Multinomial("N", 8, [0.3, 0.2, 0.1, 0.4])
    ]

    size = 3
    scipy = import_module('scipy')
    if not scipy:
        skip('Scipy not installed. Abort tests for _sample_scipy.')
    else:
        for X in distribs_scipy:
            samps = sample(X, size=size)
            samps2 = sample(X, size=(2, 2))
            for sam in samps:
                assert tuple(sam) in X.pspace.distribution.set
            for i in range(2):
                for j in range(2):
                    assert tuple(samps2[i][j]) in X.pspace.distribution.set
        N_c = NegativeMultinomial('N', 3, 0.1, 0.1, 0.1)
        raises(NotImplementedError, lambda: sample(N_c))


def test_sample_scipy():
    distribs_scipy = [
        MatrixNormal('M', [[5, 6]], [4], [[2, 1], [1, 2]]),
        Wishart('W', 5, [[1, 0], [0, 1]])
    ]

    size = 5
    scipy = import_module('scipy')
    if not scipy:
        skip('Scipy not installed. Abort tests for _sample_scipy.')
    else:
        for X in distribs_scipy:
            samps = sample(X, size=size)
            for sam in samps:
                assert Matrix(sam) in X.pspace.distribution.set
        M = MatrixGamma('M', 1, 2, [[1, 0], [0, 1]])
        raises(NotImplementedError, lambda: sample(M, size=3))


def test_sample_scipy():
    distribs_scipy = [
        Beta("B", 1, 1),
        BetaPrime("BP", 1, 1),
        Cauchy("C", 1, 1),
        Chi("C", 1),
        Normal("N", 0, 1),
        Gamma("G", 2, 7),
        GammaInverse("GI", 1, 1),
        GaussianInverse("GUI", 1, 1),
        Exponential("E", 2),
        LogNormal("LN", 0, 1),
        Pareto("P", 1, 1),
        StudentT("S", 2),
        ChiSquared("CS", 2),
        Uniform("U", 0, 1)
    ]
    size = 3
    scipy = import_module('scipy')
    if not scipy:
        skip('Scipy is not installed. Abort tests for _sample_scipy.')
    else:
        for X in distribs_scipy:
            samps = sample(X, size=size, library='scipy')
            samps2 = sample(X, size=(2, 2), library='scipy')
            for sam in samps:
                assert sam in X.pspace.domain.set
            for i in range(2):
                for j in range(2):
                    assert samps2[i][j] in X.pspace.domain.set


def test_sample_scipy():
    p = S(2)/3
    x = Symbol('x', integer=True, positive=True)
    pdf = p*(1 - p)**(x - 1) # pdf of Geometric Distribution
    distribs_scipy = [
        DiscreteRV(x, pdf, set=S.Naturals),
        Geometric('G', 0.5),
        Logarithmic('L', 0.5),
        NegativeBinomial('N', 5, 0.4),
        Poisson('P', 1),
        Skellam('S', 1, 1),
        YuleSimon('Y', 1),
        Zeta('Z', 2)
    ]
    size = 3
    scipy = import_module('scipy')
    if not scipy:
        skip('Scipy is not installed. Abort tests for _sample_scipy.')
    else:
        for X in distribs_scipy:
            samps = sample(X, size=size, library='scipy')
            samps2 = sample(X, size=(2, 2), library='scipy')
            for sam in samps:
                assert sam in X.pspace.domain.set
            for i in range(2):
                for j in range(2):
                    assert samps2[i][j] in X.pspace.domain.set


def test_sample_scipy():
    distribs_scipy = [
        FiniteRV('F', {1: S.Half, 2: Rational(1, 4), 3: Rational(1, 4)}),
        DiscreteUniform("Y", list(range(5))),
        Die("D"),
        Bernoulli("Be", 0.3),
        Binomial("Bi", 5, 0.4),
        BetaBinomial("Bb", 2, 1, 1),
        Hypergeometric("H", 1, 1, 1),
        Rademacher("R")
    ]

    size = 3
    scipy = import_module('scipy')
    if not scipy:
        skip('Scipy not installed. Abort tests for _sample_scipy.')
    else:
        for X in distribs_scipy:
            samps = sample(X, size=size)
            samps2 = sample(X, size=(2, 2))
            for sam in samps:
                assert sam in X.pspace.domain.set
            for i in range(2):
                for j in range(2):
                    assert samps2[i][j] in X.pspace.domain.set

