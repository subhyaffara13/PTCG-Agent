
def test_DomainMatrix_cancel_denom_elementwise():
    A = DM([[2, 4], [6, 8]], ZZ)
    numers, denoms = A.cancel_denom_elementwise(ZZ(1))
    assert numers == DM([[2, 4], [6, 8]], ZZ)
    assert denoms == DM([[1, 1], [1, 1]], ZZ)
    numers, denoms = A.cancel_denom_elementwise(ZZ(4))
    assert numers == DM([[1, 1], [3, 2]], ZZ)
    assert denoms == DM([[2, 1], [2, 1]], ZZ)

    raises(ZeroDivisionError, lambda: A.cancel_denom_elementwise(ZZ(0)))

