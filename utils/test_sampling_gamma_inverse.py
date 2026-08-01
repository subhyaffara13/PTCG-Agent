
def test_sampling_gamma_inverse():
    scipy = import_module('scipy')
    if not scipy:
        skip('Scipy not installed. Abort tests for sampling of gamma inverse.')
    X = GammaInverse("x", 1, 1)
    assert sample(X) in X.pspace.domain.set

