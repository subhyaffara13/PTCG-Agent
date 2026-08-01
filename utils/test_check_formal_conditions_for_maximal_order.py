
def test_check_formal_conditions_for_maximal_order():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    B = A.submodule_from_matrix(2 * DomainMatrix.eye(4, ZZ))
    C = B.submodule_from_matrix(3 * DomainMatrix.eye(4, ZZ))
    D = A.submodule_from_matrix(DomainMatrix.eye(4, ZZ)[:, :-1])
    # Is a direct submodule of a power basis, but lacks 1 as first generator:
    raises(StructureError, lambda: _check_formal_conditions_for_maximal_order(B))
    # Is not a direct submodule of a power basis:
    raises(StructureError, lambda: _check_formal_conditions_for_maximal_order(C))
    # Is direct submod of pow basis, and starts with 1, but not sq/max rank/HNF:
    raises(StructureError, lambda: _check_formal_conditions_for_maximal_order(D))

