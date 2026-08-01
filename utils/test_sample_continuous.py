
def test_sample_continuous():
    z = Symbol('z')
    Z = ContinuousRV(z, exp(-z), set=Interval(0, oo))
    assert density(Z)(-1) == 0

    scipy = import_module('scipy')
    if not scipy:
        skip('Scipy is not installed. Abort tests')
    assert sample(Z) in Z.pspace.domain.set
    sym, val = list(Z.pspace.sample().items())[0]
    assert sym == Z and val in Interval(0, oo)

    libraries = ['scipy', 'numpy', 'pymc']
    for lib in libraries:
        try:
            imported_lib = import_module(lib)
            if imported_lib:
                s0, s1, s2 = [], [], []
                s0 = sample(Z, size=10, library=lib, seed=0)
                s1 = sample(Z, size=10, library=lib, seed=0)
                s2 = sample(Z, size=10, library=lib, seed=1)
                assert all(s0 == s1)
                assert all(s1 != s2)
        except NotImplementedError:
            continue

