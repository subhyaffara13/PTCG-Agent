
def test_Matrix_inv(name, A, A_inv, den):

    def _check(**kwargs):
        if den != 0:
            assert A.inv(**kwargs) == A_inv
        else:
            raises(NonInvertibleMatrixError, lambda: A.inv(**kwargs))

    K = A.domain
    A = A.to_Matrix()
    A_inv = A_inv.to_Matrix() / K.to_sympy(den)
    _check()
    for method in ['GE', 'LU', 'ADJ', 'CH', 'LDL', 'QR']:
        _check(method=method)

