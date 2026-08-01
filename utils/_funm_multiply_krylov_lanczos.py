
def _funm_multiply_krylov_lanczos(A, b, bnorm, V, H, m):
    """
    The Lanczos iteration for constructing the basis V and the projection H = V * A V
    for the Krylov subspace Km(A, b) of order m. A must be Hermitian.

    Parameters
    ----------
    A : transposable linear operator
        The operator whose matrix function is of interest.
    b : ndarray
        The vector b to multiply the f(A) with.
    V : ndarray
        The n x (m + 1) matrix whose columns determines the basis for
        Krylov subspace Km(A, b).
    H : ndarray
        A (m + 1) x m upper Hessenberg matrix representing the projection of A
        onto Km(A, b).
    m : int
        The order of the Krylov subspace.

    Returns
    -------
    breakdown : bool
        Indicate if the Arnoldi broke down or not

    iter : int
        Returns the last valid iteration.

    """
    dotprod = np.vdot if np.iscomplexobj(b) else np.dot
    norm_tol = np.finfo(b.dtype.char).eps ** 2
    V[:, 0] = b / bnorm

    for k in range(0, m):
        if k > 0:
            V[:, k + 1] = A.dot(V[:, k]) - H[k, k - 1] * V[:, k - 1]
        else:
            V[:, k + 1] = A.dot(V[:, k])

        H[k, k] = dotprod(V[:, k + 1], V[:, k])
        V[:, k + 1] = V[:, k + 1] - H[k, k] * V[:, k]

        H[k + 1, k] = norm(V[:, k + 1])

        if H[k + 1, k] < norm_tol:
            return True, k

        V[:, k + 1] = V[:, k + 1] / H[k + 1, k]
        if k < m - 1:
            H[k, k + 1] = H[k + 1, k]

    return False, m

