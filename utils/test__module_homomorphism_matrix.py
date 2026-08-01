
def test_ModuleHomomorphism_matrix():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    phi = ModuleEndomorphism(A, lambda a: a ** 2)
    M = phi.matrix()
    assert M == DomainMatrix([
        [1, 0, -1, 0],
        [0, 0, -1, 1],
        [0, 1, -1, 0],
        [0, 0, -1, 0]
    ], (4, 4), ZZ)

