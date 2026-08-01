
def _logdet_difference_matrix(order, n):
    """Logarithm of the determinant of the difference matrix.

    If D is the difference matrix of order=p, then this computes `log det(D @ D.T)`
    which equals the sum of the log of non-zero eigenvalues of `D.T @ D`.
    """
    # product of eigenvalues =
    # prod(binom(n+i-1, 2i-1), i=1..p) / prod(binom(2i, i), i=1..p-1)
    # How to derive this formula? Well, ... some magic.
    p = order
    if order == 1:
        return np.log(n)
    logdet = 0.0
    for i in range(1, p+1):
        logdet += np.log(binom(n + i - 1, 2*i - 1) / binom(2*i, i)) 
    logdet += np.log(binom(2*p, p))
    return logdet

