
def test_sampling_gaussian_inverse():
    scipy = import_module('scipy')
    if not scipy:
        skip('Scipy not installed. Abort tests for sampling of Gaussian inverse.')
    X = GaussianInverse("x", 1, 1)
    assert sample(X, library='scipy') in X.pspace.domain.set

