
def test_sample_numpy():
    distribs_numpy = [
        MultivariateNormal("M", [3, 4], [[2, 1], [1, 2]]),
        MultivariateBeta("B", [0.4, 5, 15, 50, 203]),
        Multinomial("N", 50, [0.3, 0.2, 0.1, 0.25, 0.15])
    ]
    size = 3
    numpy = import_module('numpy')
    if not numpy:
        skip('Numpy is not installed. Abort tests for _sample_numpy.')
    else:
        for X in distribs_numpy:
            samps = sample(X, size=size, library='numpy')
            for sam in samps:
                assert tuple(sam) in X.pspace.distribution.set
        N_c = NegativeMultinomial('N', 3, 0.1, 0.1, 0.1)
        raises(NotImplementedError, lambda: sample(N_c, library='numpy'))


def test_sample_numpy():
    distribs_numpy = [
        Beta("B", 1, 1),
        Normal("N", 0, 1),
        Gamma("G", 2, 7),
        Exponential("E", 2),
        LogNormal("LN", 0, 1),
        Pareto("P", 1, 1),
        ChiSquared("CS", 2),
        Uniform("U", 0, 1),
        FDistribution("FD", 1, 2),
        Gumbel("GB", 1, 2),
        Laplace("L", 1, 2),
        Logistic("LO", 1, 2),
        Rayleigh("R", 1),
        Triangular("T", 1, 2, 2),
    ]
    size = 3
    numpy = import_module('numpy')
    if not numpy:
        skip('Numpy is not installed. Abort tests for _sample_numpy.')
    else:
        for X in distribs_numpy:
            samps = sample(X, size=size, library='numpy')
            for sam in samps:
                assert sam in X.pspace.domain.set
        raises(NotImplementedError,
               lambda: sample(Chi("C", 1), library='numpy'))
    raises(NotImplementedError,
           lambda: Chi("C", 1).pspace.distribution.sample(library='tensorflow'))


def test_sample_numpy():
    distribs_numpy = [
        Geometric('G', 0.5),
        Poisson('P', 1),
        Zeta('Z', 2)
    ]
    size = 3
    numpy = import_module('numpy')
    if not numpy:
        skip('Numpy is not installed. Abort tests for _sample_numpy.')
    else:
        for X in distribs_numpy:
            samps = sample(X, size=size, library='numpy')
            for sam in samps:
                assert sam in X.pspace.domain.set
        raises(NotImplementedError,
               lambda: sample(Skellam('S', 1, 1), library='numpy'))
    raises(NotImplementedError,
           lambda: Skellam('S', 1, 1).pspace.distribution.sample(library='tensorflow'))


def test_sample_numpy():
    distribs_numpy = [
        Binomial("B", 5, 0.4),
        Hypergeometric("H", 2, 1, 1)
    ]
    size = 3
    numpy = import_module('numpy')
    if not numpy:
        skip('Numpy is not installed. Abort tests for _sample_numpy.')
    else:
        for X in distribs_numpy:
            samps = sample(X, size=size, library='numpy')
            for sam in samps:
                assert sam in X.pspace.domain.set
        raises(NotImplementedError,
               lambda: sample(Die("D"), library='numpy'))
    raises(NotImplementedError,
           lambda: Die("D").pspace.sample(library='tensorflow'))

