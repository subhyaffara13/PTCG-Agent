
def _remove_redundancy_svd(A, b):
    """
    Eliminates redundant equations from system of equations defined by Ax = b
    and identifies infeasibilities.

    Parameters
    ----------
    A : 2-D array
        An array representing the left-hand side of a system of equations
    b : 1-D array
        An array representing the right-hand side of a system of equations

    Returns
    -------
    A : 2-D array
        An array representing the left-hand side of a system of equations
    b : 1-D array
        An array representing the right-hand side of a system of equations
    status: int
        An integer indicating the status of the system
        0: No infeasibility identified
        2: Trivially infeasible
    message : str
        A string descriptor of the exit status of the optimization.

    References
    ----------
    .. [2] Andersen, Erling D. "Finding all linearly dependent rows in
           large-scale linear programming." Optimization Methods and Software
           6.3 (1995): 219-227.

    """

    A, b, status, message = _remove_zero_rows(A, b)

    if status != 0:
        return A, b, status, message

    U, s, Vh = svd(A)
    eps = np.finfo(float).eps
    tol = s.max() * max(A.shape) * eps

    m, n = A.shape
    s_min = s[-1] if m <= n else 0

    # this algorithm is faster than that of [2] when the nullspace is small
    # but it could probably be improvement by randomized algorithms and with
    # a sparse implementation.
    # it relies on repeated singular value decomposition to find linearly
    # dependent rows (as identified by columns of U that correspond with zero
    # singular values). Unfortunately, only one row can be removed per
    # decomposition (I tried otherwise; doing so can cause problems.)
    # It would be nice if we could do truncated SVD like sp.sparse.linalg.svds
    # but that function is unreliable at finding singular values near zero.
    # Finding max eigenvalue L of A A^T, then largest eigenvalue (and
    # associated eigenvector) of -A A^T + L I (I is identity) via power
    # iteration would also work in theory, but is only efficient if the
    # smallest nonzero eigenvalue of A A^T is close to the largest nonzero
    # eigenvalue.

    while abs(s_min) < tol:
        v = U[:, -1]  # TODO: return these so user can eliminate from problem?
        # rows need to be represented in significant amount
        eligibleRows = np.abs(v) > tol * 10e6
        if not np.any(eligibleRows) or np.any(np.abs(v.dot(A)) > tol):
            status = 4
            message = ("Due to numerical issues, redundant equality "
                       "constraints could not be removed automatically. "
                       "Try providing your constraint matrices as sparse "
                       "matrices to activate sparse presolve, try turning "
                       "off redundancy removal, or try turning off presolve "
                       "altogether.")
            break
        if np.any(np.abs(v.dot(b)) > tol * 100):  # factor of 100 to fix 10038 and 10349
            status = 2
            message = ("There is a linear combination of rows of A_eq that "
                       "results in zero, suggesting a redundant constraint. "
                       "However the same linear combination of b_eq is "
                       "nonzero, suggesting that the constraints conflict "
                       "and the problem is infeasible.")
            break

        i_remove = _get_densest(A, eligibleRows)
        A = np.delete(A, i_remove, axis=0)
        b = np.delete(b, i_remove)
        U, s, Vh = svd(A)
        m, n = A.shape
        s_min = s[-1] if m <= n else 0

    return A, b, status, message

