
def _bidiagonal_decmp_hholder(M):
    m = M.rows
    n = M.cols
    A = M.as_mutable()
    U, V = A.eye(m), A.eye(n)
    for i in range(min(m, n)):
        v, bet = _householder_vector(A[i:, i])
        hh_mat = A.eye(m - i) - bet * v * v.H
        A[i:, i:] = hh_mat * A[i:, i:]
        temp = A.eye(m)
        temp[i:, i:] = hh_mat
        U = U * temp
        if i + 1 <= n - 2:
            v, bet = _householder_vector(A[i, i+1:].T)
            hh_mat = A.eye(n - i - 1) - bet * v * v.H
            A[i:, i+1:] = A[i:, i+1:] * hh_mat
            temp = A.eye(n)
            temp[i+1:, i+1:] = hh_mat
            V = temp * V
    return U, A, V

