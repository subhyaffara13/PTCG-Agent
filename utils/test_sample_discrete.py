
def test_sample_discrete():
    X = Geometric('X', S.Half)
    scipy = import_module('scipy')
    if not scipy:
        skip('Scipy not installed. Abort tests')
    assert sample(X) in X.pspace.domain.set
    samps = sample(X, size=2) # This takes long time if ran without scipy
    for samp in samps:
        assert samp in X.pspace.domain.set

    libraries = ['scipy', 'numpy', 'pymc']
    for lib in libraries:
        try:
            imported_lib = import_module(lib)
            if imported_lib:
                s0, s1, s2 = [], [], []
                s0 = sample(X, size=10, library=lib, seed=0)
                s1 = sample(X, size=10, library=lib, seed=0)
                s2 = sample(X, size=10, library=lib, seed=1)
                assert all(s0 == s1)
                assert not all(s1 == s2)
        except NotImplementedError:
            continue

