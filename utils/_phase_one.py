
def _phase_one(A, b, x0, callback, postsolve_args, maxiter, tol, disp,
               maxupdate, mast, pivot):
    """
    The purpose of phase one is to find an initial basic feasible solution
    (BFS) to the original problem.

    Generates an auxiliary problem with a trivial BFS and an objective that
    minimizes infeasibility of the original problem. Solves the auxiliary
    problem using the main simplex routine (phase two). This either yields
    a BFS to the original problem or determines that the original problem is
    infeasible. If feasible, phase one detects redundant rows in the original
    constraint matrix and removes them, then chooses additional indices as
    necessary to complete a basis/BFS for the original problem.
    """

    m, n = A.shape
    status = 0

    # generate auxiliary problem to get initial BFS
    A, b, c, basis, x, status = _generate_auxiliary_problem(A, b, x0, tol)

    if status == 6:
        residual = c.dot(x)
        iter_k = 0
        return x, basis, A, b, residual, status, iter_k

    # solve auxiliary problem
    phase_one_n = n
    iter_k = 0
    x, basis, status, iter_k = _phase_two(c, A, x, basis, callback,
                                          postsolve_args,
                                          maxiter, tol, disp,
                                          maxupdate, mast, pivot,
                                          iter_k, phase_one_n)

    # check for infeasibility
    residual = c.dot(x)
    if status == 0 and residual > tol:
        status = 2

    # drive artificial variables out of basis
    # TODO: test redundant row removal better
    # TODO: make solve more efficient with BGLU? This could take a while.
    keep_rows = np.ones(m, dtype=bool)
    for basis_column in basis[basis >= n]:
        B = A[:, basis]
        try:
            basis_finder = np.abs(solve(B, A))  # inefficient
            pertinent_row = np.argmax(basis_finder[:, basis_column])
            eligible_columns = np.ones(n, dtype=bool)
            eligible_columns[basis[basis < n]] = 0
            eligible_column_indices = np.where(eligible_columns)[0]
            index = np.argmax(basis_finder[:, :n]
                              [pertinent_row, eligible_columns])
            new_basis_column = eligible_column_indices[index]
            if basis_finder[pertinent_row, new_basis_column] < tol:
                keep_rows[pertinent_row] = False
            else:
                basis[basis == basis_column] = new_basis_column
        except LinAlgError:
            status = 4

    # form solution to original problem
    A = A[keep_rows, :n]
    basis = basis[keep_rows]
    x = x[:n]
    m = A.shape[0]
    return x, basis, A, b, residual, status, iter_k

