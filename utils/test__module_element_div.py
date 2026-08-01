
def test_ModuleElement_div():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    C = A.submodule_from_matrix(3 * DomainMatrix.eye(4, ZZ))
    e = A(to_col([0, 2, 0, 0]), denom=3)
    f = A(to_col([0, 0, 0, 7]), denom=5)
    g = C(to_col([1, 1, 1, 1]))
    assert e // f == 10*A(3)//21
    assert e // g == -2*A(2)//9
    assert 3 // g == -A(1)

