
def test_lognormal_sampling():
    # Right now, only density function and sampling works
    scipy = import_module('scipy')
    if not scipy:
        skip('Scipy is not installed. Abort tests')
    for i in range(3):
        X = LogNormal('x', i, 1)
        assert sample(X) in X.pspace.domain.set

    size = 5
    samps = sample(X, size=size)
    for samp in samps:
        assert samp in X.pspace.domain.set

