
def test_sample_pymc():
    distribs_pymc = [
        MultivariateNormal("M", [5, 2], [[1, 0], [0, 1]]),
        MultivariateBeta("B", [0.4, 5, 15]),
        Multinomial("N", 4, [0.3, 0.2, 0.1, 0.4])
    ]
    size = 3
    pymc = import_module('pymc')
    if not pymc:
        skip('PyMC is not installed. Abort tests for _sample_pymc.')
    else:
        for X in distribs_pymc:
            samps = sample(X, size=size, library='pymc')
            for sam in samps:
                assert tuple(sam.flatten()) in X.pspace.distribution.set
        N_c = NegativeMultinomial('N', 3, 0.1, 0.1, 0.1)
        raises(NotImplementedError, lambda: sample(N_c, library='pymc'))


def test_sample_pymc():
    distribs_pymc = [
        MatrixNormal('M', [[5, 6], [3, 4]], [[1, 0], [0, 1]], [[2, 1], [1, 2]]),
        Wishart('W', 7, [[2, 1], [1, 2]])
    ]
    size = 3
    pymc = import_module('pymc')
    if not pymc:
        skip('PyMC is not installed. Abort tests for _sample_pymc.')
    else:
        for X in distribs_pymc:
            samps = sample(X, size=size, library='pymc')
            for sam in samps:
                assert Matrix(sam) in X.pspace.distribution.set
        M = MatrixGamma('M', 1, 2, [[1, 0], [0, 1]])
        raises(NotImplementedError, lambda: sample(M, size=3))


def test_sample_pymc():
    distribs_pymc = [
        Beta("B", 1, 1),
        Cauchy("C", 1, 1),
        Normal("N", 0, 1),
        Gamma("G", 2, 7),
        GaussianInverse("GI", 1, 1),
        Exponential("E", 2),
        LogNormal("LN", 0, 1),
        Pareto("P", 1, 1),
        ChiSquared("CS", 2),
        Uniform("U", 0, 1)
    ]
    size = 3
    pymc = import_module('pymc')
    if not pymc:
        skip('PyMC is not installed. Abort tests for _sample_pymc.')
    else:
        for X in distribs_pymc:
            samps = sample(X, size=size, library='pymc')
            for sam in samps:
                assert sam in X.pspace.domain.set
        raises(NotImplementedError,
               lambda: sample(Chi("C", 1), library='pymc'))


def test_sample_pymc():
    distribs_pymc = [
        Geometric('G', 0.5),
        Poisson('P', 1),
        NegativeBinomial('N', 5, 0.4)
    ]
    size = 3
    pymc = import_module('pymc')
    if not pymc:
        skip('PyMC is not installed. Abort tests for _sample_pymc.')
    else:
        for X in distribs_pymc:
            samps = sample(X, size=size, library='pymc')
            for sam in samps:
                assert sam in X.pspace.domain.set
        raises(NotImplementedError,
               lambda: sample(Skellam('S', 1, 1), library='pymc'))


def test_sample_pymc():
    distribs_pymc = [
        Bernoulli('B', 0.2),
        Binomial('N', 5, 0.4)
    ]
    size = 3
    pymc = import_module('pymc')
    if not pymc:
        skip('PyMC is not installed. Abort tests for _sample_pymc.')
    else:
        for X in distribs_pymc:
            samps = sample(X, size=size, library='pymc')
            for sam in samps:
                assert sam in X.pspace.domain.set
        raises(NotImplementedError,
                          lambda: (sample(Die("D"), library='pymc')))

