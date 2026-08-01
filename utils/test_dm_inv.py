
def test_dm_inv(name, A, A_inv, den):
    A = A.to_field()
    if den != 0:
        A_inv = A_inv.to_field() / den
        assert A.inv() == A_inv
    else:
        raises(DMNonInvertibleMatrixError, lambda: A.inv())

