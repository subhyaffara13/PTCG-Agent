
def _solve_WH_banded(y, lamb, order=2, weights=None, calc_logdet=False, warn_user=True):
    """
    Solve the WH optimization problem via the normal equations.
    
    A @ x = y
    A = I + lamb * P = I + lamb * D' @ D
    D = difference matrix of order=`order` 

    With weights W = diag(weights):
    A = W + lamb * P
    A @ x = W @ y

    Returns
    -------
    x : ndarray
        The solution.
    logdet : float
        Logarithm of the determinant of matrix A. Returns 0 if ``calc_logdet=False``.
    """
    n = y.shape[0]  # n >= p + 1 was already checked
    p = order  # order of difference penalty
    # Construct penalty matrix P = D'D of shape (n-p, n) as if n = 2p+1 (to save
    # memory).
    if n < 2*p + 1:
        D = np.diff(np.eye(n), n=p, axis=0)  # shape (n-p, n)
    else:
        D = np.diff(np.eye(2*p + 1), n=p, axis=0)  # shape (p+1, 2p+1)
    P_raw = D.T @ D  # shape (2p+1, 2p+1) if n >= 2p+1 else (n, n)

    # Because our matrix A = np.eye(n, dtype=np.float64) + lamb * (D.T @ D) is
    # symmetric and banded with u = l = p, we construct it in the lower "ab"-format
    # for use in solveh_banded, i.e. each row in ab is a subdiagonal of A:
    #   ab[0, :]   = np.diagonal(A, 0)
    #   ab[1, :-1] = np.diagonal(A, 1)
    #   ab[2, :-2] = np.diagonal(A, 2)
    #   ..
    ab = np.zeros((p + 1, min(2*p + 1, n)))
    for i in range(p + 1):
        ab[i, :ab.shape[1] - i] = np.diagonal(P_raw, i)
    ab *= lamb
    if n > 2*p + 1:
        ab = np.concat(
            [
                ab[:, :p+1],
                np.repeat(ab[:, p:p+1], n - (2*p+1), axis=1),
                ab[:, -p:],
            ],
            axis=1,
        )

    if weights is None:
        # Check if lambda is so large that A = I + lambda D'D = lambda D'D. We even add
        # a factor of 8, i.e. A should have at least 4 bits from I (not only D'D).
        # Note that the minimal diagonal element of D'D is always 1.
        if lamb * np.finfo(np.float64).eps > 8:
            # If lambda approaches infinity, WH approaches a polynomial fit.
            x, logdet = _polynomial_fit(
                y, lamb=lamb, order=order, calc_logdet=calc_logdet
            )
            info = 0
        else:
            ab[0, :] += 1.0  # This corresponds to np.eye(n).
            x, logdet, info = _solveh_banded(ab, y, calc_logdet=calc_logdet)
    else:
        if (ab[0, :] == ab[0, :] + weights * 8).all():
            # If lambda approaches infinity, WH approaches a polynomial fit.
            x, logdet = _polynomial_fit(
                y, lamb=lamb, order=order, weights=weights, calc_logdet=calc_logdet
            )
            info = 0
        else:
            ab[0, :] += weights
            x, logdet, info = _solveh_banded(ab, weights * y, calc_logdet=calc_logdet)

    if info > 0:
        # LinAlgError(f"{info}th leading minor not positive definite")
        # For very large values of lamb, we know that
        #   - the linear solver breaks down
        #   - the solution approaches a polynomial least squares fit of degree
        #     order - 1.
        # Note that for a certain large lamb, WH already reaches the polynomial least
        # squares fit almost exactly. For larger lamb, WH starts to deviate from the
        # polynomial (=worse solution due to numerical instability), until the solver
        # breaks down and reports info > 0.
        if warn_user:
            msg_weights = "" if weights is None else " or due to the weights"
            msg = (
                "The linear solver in Whittaker-Henderson smoothing detected a "
                "numerical instability. This is likely due to a very large value of "
                f"{lamb=}"
                + msg_weights + ". "
                "As Whittaker-Henderson approaches a polynomial of degree 'order - 1' "
                "for large lamb, this polynomial (via least squares) is returned."
            )
            warnings.warn(msg, UserWarning, stacklevel=2)
        x, logdet = _polynomial_fit(
            y, lamb, order=order, weights=weights, calc_logdet=calc_logdet
        )
    return x, logdet

