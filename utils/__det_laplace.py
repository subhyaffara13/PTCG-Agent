
def __det_laplace(M):
    """Compute the determinant of a matrix using Laplace expansion.

    This is a recursive function, and it should not be called directly.
    Use _det_laplace() instead. The reason for splitting this function
    into two is to allow caching of determinants of submatrices. While
    one could also define this function inside _det_laplace(), that
    would remove the advantage of using caching in Cramer Solve.
    """
    n = M.shape[0]
    if n == 1:
        return M[0]
    elif n == 2:
        return M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]
    else:
        return sum((-1) ** i * M[0, i] *
                   __det_laplace(M.minor_submatrix(0, i)) for i in range(n))

