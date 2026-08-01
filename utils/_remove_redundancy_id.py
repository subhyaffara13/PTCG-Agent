
def _remove_redundancy_id(A, rhs, rank=None, randomized=True):
    """Eliminates redundant equations from a system of equations.

    Eliminates redundant equations from system of equations defined by Ax = b
    and identifies infeasibilities.

    Parameters
    ----------
    A : 2-D array
        An array representing the left-hand side of a system of equations
    rhs : 1-D array
        An array representing the right-hand side of a system of equations
    rank : int, optional
        The rank of A
    randomized: bool, optional
        True for randomized interpolative decomposition

    Returns
    -------
    A : 2-D array
        An array representing the left-hand side of a system of equations
    rhs : 1-D array
        An array representing the right-hand side of a system of equations
    status: int
        An integer indicating the status of the system
        0: No infeasibility identified
        2: Trivially infeasible
    message : str
        A string descriptor of the exit status of the optimization.

    """

    status = 0
    message = ""
    inconsistent = ("There is a linear combination of rows of A_eq that "
                    "results in zero, suggesting a redundant constraint. "
                    "However the same linear combination of b_eq is "
                    "nonzero, suggesting that the constraints conflict "
                    "and the problem is infeasible.")

    A, rhs, status, message = _remove_zero_rows(A, rhs)

    if status != 0:
        return A, rhs, status, message

    m, n = A.shape

    k = rank
    if rank is None:
        k = np.linalg.matrix_rank(A)

    idx, proj = interp_decomp(A.T, k, rand=randomized)

    # first k entries in idx are indices of the independent rows
    # remaining entries are the indices of the m-k dependent rows
    # proj provides a linear combinations of rows of A2 that form the
    # remaining m-k (dependent) rows. The same linear combination of entries
    # in rhs2 must give the remaining m-k entries. If not, the system is
    # inconsistent, and the problem is infeasible.
    if not np.allclose(rhs[idx[:k]] @ proj, rhs[idx[k:]]):
        status = 2
        message = inconsistent

    # sort indices because the other redundancy removal routines leave rows
    # in original order and tests were written with that in mind
    idx = sorted(idx[:k])
    A2 = A[idx, :]
    rhs2 = rhs[idx]
    return A2, rhs2, status, message

