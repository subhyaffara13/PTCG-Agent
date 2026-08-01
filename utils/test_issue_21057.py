
def test_issue_21057():
    m = Normal("x", [0, 0], [[0, 0], [0, 0]])
    n = MultivariateNormal("x", [0, 0], [[0, 0], [0, 0]])
    p = Normal("x", [0, 0], [[0, 0], [0, 1]])
    assert m == n
    libraries = ('scipy', 'numpy')  # , 'pymc')  # <-- pymc fails
    for library in libraries:
        try:
            imported_lib = import_module(library)
            if imported_lib:
                s1 = sample(m, size=8, library=library)
                s2 = sample(n, size=8, library=library)
                s3 = sample(p, size=8, library=library)
                assert tuple(s1.flatten()) == tuple(s2.flatten())
                for s in s3:
                    assert tuple(s.flatten()) in p.pspace.distribution.set
        except NotImplementedError:
            continue

