
def _remove_redundancy_pivot_sparse(A, rhs):
    """
    Eliminates redundant equations from system of equations defined by Ax = b
    and identifies infeasibilities.

    Parameters
    ----------
    A : 2-D sparse array
        An matrix representing the left-hand side of a system of equations
    rhs : 1-D array
        An array representing the right-hand side of a system of equations

    Returns
    -------
    A : 2-D sparse array
        A matrix representing the left-hand side of a system of equations
    rhs : 1-D array
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

    tolapiv = 1e-8
    tolprimal = 1e-8
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

    v = list(range(m))      # Artificial column indices.
    b = list(v)             # Basis column indices.
    # This is better as a list than a set because column order of basis matrix
    # needs to be consistent.
    k = set(range(m, m+n))  # Structural column indices.
    d = []                  # Indices of dependent rows

    A_orig = A
    A = scipy.sparse.hstack((scipy.sparse.eye_array(m), A)).tocsc()
    e = np.zeros(m)

    # Implements basic algorithm from [2]
    # Uses only one of the suggested improvements (removing zero rows).
    # Removing column singletons would be easy, but it is not as important
    # because the procedure is performed only on the equality constraint
    # matrix from the original problem - not on the canonical form matrix,
    # which would have many more column singletons due to slack variables
    # from the inequality constraints.
    # The thoughts on "crashing" the initial basis sound useful, but the
    # description of the procedure seems to assume a lot of familiarity with
    # the subject; it is not very explicit. I already went through enough
    # trouble getting the basic algorithm working, so I was not interested in
    # trying to decipher this, too. (Overall, the paper is fraught with
    # mistakes and ambiguities - which is strange, because the rest of
    # Andersen's papers are quite good.)
    # I tried and tried and tried to improve performance using the
    # Bartels-Golub update. It works, but it's only practical if the LU
    # factorization can be specialized as described, and that is not possible
    # until the SciPy SuperLU interface permits control over column
    # permutation - see issue #7700.

    for i in v:
        B = A[:, b]

        e[i] = 1
        if i > 0:
            e[i-1] = 0

        pi = scipy.sparse.linalg.spsolve(B.transpose(), e).reshape(-1, 1)

        js = list(k-set(b))  # not efficient, but this is not the time sink...

        # Due to overhead, it tends to be faster (for problems tested) to
        # compute the full matrix-vector product rather than individual
        # vector-vector products (with the chance of terminating as soon
        # as any are nonzero). For very large matrices, it might be worth
        # it to compute, say, 100 or 1000 at a time and stop when a nonzero
        # is found.

        c = (np.abs(A[:, js].transpose().dot(pi)) > tolapiv).nonzero()[0]
        if len(c) > 0:  # independent
            j = js[c[0]]
            # in a previous commit, the previous line was changed to choose
            # index j corresponding with the maximum dot product.
            # While this avoided issues with almost
            # singular matrices, it slowed the routine in most NETLIB tests.
            # I think this is because these columns were denser than the
            # first column with nonzero dot product (c[0]).
            # It would be nice to have a heuristic that balances sparsity with
            # high dot product, but I don't think it's worth the time to
            # develop one right now. Bartels-Golub update is a much higher
            # priority.
            b[i] = j  # replace artificial column
        else:
            bibar = pi.T.dot(rhs.reshape(-1, 1))
            bnorm = np.linalg.norm(rhs)
            if abs(bibar)/(1 + bnorm) > tolprimal:
                status = 2
                message = inconsistent
                return A_orig, rhs, status, message
            else:  # dependent
                d.append(i)

    keep = set(range(m))
    keep = list(keep - set(d))
    return A_orig[keep, :], rhs[keep], status, message

