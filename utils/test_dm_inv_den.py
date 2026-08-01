
def test_dm_inv_den(name, A, A_inv, den):
    if den != 0:
        A_inv_f, den_f = A.inv_den()
        assert A_inv_f.cancel_denom(den_f) == A_inv.cancel_denom(den)
    else:
        raises(DMNonInvertibleMatrixError, lambda: A.inv_den())

