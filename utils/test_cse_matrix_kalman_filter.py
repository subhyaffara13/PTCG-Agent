
def test_cse_matrix_kalman_filter():
    """Kalman Filter example from Matthew Rocklin's SciPy 2013 talk.

    Talk titled: "Matrix Expressions and BLAS/LAPACK; SciPy 2013 Presentation"

    Video: https://pyvideo.org/scipy-2013/matrix-expressions-and-blaslapack-scipy-2013-pr.html

    Notes
    =====

    Equations are:

    new_mu = mu + Sigma*H.T * (R + H*Sigma*H.T).I * (H*mu - data)
           = MatAdd(mu, MatMul(Sigma, Transpose(H), Inverse(MatAdd(R, MatMul(H, Sigma, Transpose(H)))), MatAdd(MatMul(H, mu), MatMul(S.NegativeOne, data))))
    new_Sigma = Sigma - Sigma*H.T * (R + H*Sigma*H.T).I * H * Sigma
              = MatAdd(Sigma, MatMul(S.NegativeOne, Sigma, Transpose(H)), Inverse(MatAdd(R, MatMul(H*Sigma*Transpose(H)))), H, Sigma))

    """
    N = 2
    mu = ImmutableDenseMatrix(symbols(f'mu:{N}'))
    Sigma = ImmutableDenseMatrix(symbols(f'Sigma:{N * N}')).reshape(N, N)
    H = ImmutableDenseMatrix(symbols(f'H:{N * N}')).reshape(N, N)
    R = ImmutableDenseMatrix(symbols(f'R:{N * N}')).reshape(N, N)
    data = ImmutableDenseMatrix(symbols(f'data:{N}'))
    new_mu = MatAdd(mu, MatMul(Sigma, Transpose(H), Inverse(MatAdd(R, MatMul(H, Sigma, Transpose(H)))), MatAdd(MatMul(H, mu), MatMul(S.NegativeOne, data))))
    new_Sigma = MatAdd(Sigma, MatMul(S.NegativeOne, Sigma, Transpose(H), Inverse(MatAdd(R, MatMul(H, Sigma, Transpose(H)))), H, Sigma))
    cse_expr = cse([new_mu, new_Sigma])
    x0 = MatrixSymbol('x0', N, N)
    x1 = MatrixSymbol('x1', N, N)
    replacements_expected = [
        (x0, Transpose(H)),
        (x1, Inverse(MatAdd(R, MatMul(H, Sigma, x0)))),
    ]
    reduced_exprs_expected = [
        MatAdd(mu, MatMul(Sigma, x0, x1, MatAdd(MatMul(H, mu), MatMul(S.NegativeOne, data)))),
        MatAdd(Sigma, MatMul(S.NegativeOne, Sigma, x0, x1, H, Sigma)),
    ]
    assert cse_expr == (replacements_expected, reduced_exprs_expected)

