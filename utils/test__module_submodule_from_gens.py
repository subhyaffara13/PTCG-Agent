
def test_Module_submodule_from_gens():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    gens = [2*A(0), 2*A(1), 6*A(0), 6*A(1)]
    B = A.submodule_from_gens(gens)
    # Because the 3rd and 4th generators do not add anything new, we expect
    # the cols of the matrix of B to just reproduce the first two gens:
    M = gens[0].column().hstack(gens[1].column())
    assert B.matrix == M
    # At least one generator must be provided:
    raises(ValueError, lambda: A.submodule_from_gens([]))
    # All generators must belong to A:
    raises(ValueError, lambda: A.submodule_from_gens([3*A(0), B(0)]))

