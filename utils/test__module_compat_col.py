
def test_Module_compat_col():
    T = Poly(cyclotomic_poly(5, x))
    A = PowerBasis(T)
    col = to_col([1, 2, 3, 4])
    row = col.transpose()
    assert A.is_compat_col(col) is True
    assert A.is_compat_col(row) is False
    assert A.is_compat_col(1) is False
    assert A.is_compat_col(DomainMatrix.eye(3, ZZ)[:, 0]) is False
    assert A.is_compat_col(DomainMatrix.eye(4, QQ)[:, 0]) is False
    assert A.is_compat_col(DomainMatrix.eye(4, ZZ)[:, 0]) is True

