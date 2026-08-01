
def _solveh_banded(ab, b, calc_logdet=False):
    """
    Solve the equation ``a @ x = b`` for ``x``,  where ``a`` is the 
    Hermitian positive-definite banded matrix defined by `ab`.

    Same as scipy.linalg.solveh_banded(lower=True, check_finite=False), but:
    - also returns the log of the determinant and info
    - no error is raised if info > 0
    - no input validation
    - only real values, no complex
    - only `lower = True` code path
    - always overwrite_XX = False
    - b only a 1-dim array

    Parameters
    ----------
    ab : (``u`` + 1, M) array_like
        Banded matrix
    b : (M,) array_like
        Right-hand side

    Returns
    -------
    x : (M,) ndarray
        The solution to the system ``a x = b``. Shape of return matches shape of `b`.
    logdet : float
        Logarithm of the determinant of `ab`. Returns 0 if ``calc_logdet=False``.
    info : int
    """
    a1 = ab
    b1 = b
    overwrite_b = False
    overwrite_ab = False
    logdet = 0.0

    if a1.shape[0] == 2:
        method = "ptsv"
        ptsv = get_lapack_funcs(method, (a1, b1), ilp64="preferred")
        # We assume lower=True and real arrays
        d = a1[0, :]
        e = a1[1, :-1]
        # ptsv uses LDL', returnes d=diag(D), du=diag(L, -1)
        d, du, x, info = ptsv(d, e, b1, overwrite_ab, overwrite_ab, overwrite_b)
        if calc_logdet and info == 0:
            logdet = np.log(d).sum()
    else:
        method = "pbsv"
        pbsv = get_lapack_funcs(method, (a1, b1), ilp64="preferred")
        # pbsv uses Cholesky LL', returns c=L in ab-storage format
        c, x, info = pbsv(a1, b1, lower=True, overwrite_ab=overwrite_ab,
                          overwrite_b=overwrite_b)
        if calc_logdet and info == 0:
            logdet = 2 * np.log(c[0, :]).sum()
    if info < 0:
        raise ValueError(f"illegal value in {-info}th argument of internal {method}")
    return x, logdet, info

