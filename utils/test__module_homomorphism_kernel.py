
def test_ModuleHomomorphism_kernel():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    phi = ModuleEndomorphism(A, lambda a: a ** 5)
    N = phi.kernel()
    assert N.n == 3

