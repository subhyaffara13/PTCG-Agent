
def _check_fflu_result(result, A, P_ans, L_ans, D_ans, U_ans):
    P, L, D, U = result
    P = _to_DM(P, P_ans)
    L = _to_DM(L, L_ans)
    D = _to_DM(D, D_ans)
    U = _to_DM(U, U_ans)
    A = _to_DM(A, P_ans)
    m, n = A.shape
    assert P.shape == (m, m)
    assert L.shape == (m, m)
    assert D.shape == (m, m)
    assert U.shape == (m, n)
    assert L.is_lower
    assert D.is_diagonal
    di, d = D.inv_den()
    assert P.matmul(A).rmul(d) == L.matmul(di).matmul(U)
    assert U.is_upper

