
def test_DomainMatrix_cancel_denom():
    A = DM([[2, 4], [6, 8]], ZZ)
    assert A.cancel_denom(ZZ(1)) == (DM([[2, 4], [6, 8]], ZZ), ZZ(1))
    assert A.cancel_denom(ZZ(3)) == (DM([[2, 4], [6, 8]], ZZ), ZZ(3))
    assert A.cancel_denom(ZZ(4)) == (DM([[1, 2], [3, 4]], ZZ), ZZ(2))

    A = DM([[1, 2], [3, 4]], ZZ)
    assert A.cancel_denom(ZZ(2)) == (A, ZZ(2))
    assert A.cancel_denom(ZZ(-2)) == (-A, ZZ(2))

    # Test canonicalization of denominator over Gaussian rationals.
    A = DM([[1, 2], [3, 4]], QQ_I)
    assert A.cancel_denom(QQ_I(0,2)) == (QQ_I(0,-1)*A, QQ_I(2))

    raises(ZeroDivisionError, lambda: A.cancel_denom(ZZ(0)))

