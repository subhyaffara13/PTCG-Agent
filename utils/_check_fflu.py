
def _check_fflu(A, P, L, D, U):
    P_field = P.to_field().to_dense()
    L_field = L.to_field().to_dense()
    D_field = D.to_field().to_dense()
    U_field = U.to_field().to_dense()
    m, n = A.shape
    assert P_field.shape == (m, m)
    assert L_field.shape == (m, m)
    assert D_field.shape == (m, m)
    assert U_field.shape == (m, n)
    assert L_field.is_lower
    assert D_field.is_diagonal
    di, d = D.inv_den()
    assert P.matmul(A).rmul(d) == L.matmul(di).matmul(U)
    assert U_field.is_upper

