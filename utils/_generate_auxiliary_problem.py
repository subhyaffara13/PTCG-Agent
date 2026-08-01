
def _generate_auxiliary_problem(A, b, x0, tol):
    """
    Modifies original problem to create an auxiliary problem with a trivial
    initial basic feasible solution and an objective that minimizes
    infeasibility in the original problem.

    Conceptually, this is done by stacking an identity matrix on the right of
    the original constraint matrix, adding artificial variables to correspond
    with each of these new columns, and generating a cost vector that is all
    zeros except for ones corresponding with each of the new variables.

    A initial basic feasible solution is trivial: all variables are zero
    except for the artificial variables, which are set equal to the
    corresponding element of the right hand side `b`.

    Running the simplex method on this auxiliary problem drives all of the
    artificial variables - and thus the cost - to zero if the original problem
    is feasible. The original problem is declared infeasible otherwise.

    Much of the complexity below is to improve efficiency by using singleton
    columns in the original problem where possible, thus generating artificial
    variables only as necessary, and using an initial 'guess' basic feasible
    solution.
    """
    status = 0
    m, n = A.shape

    if x0 is not None:
        x = x0
    else:
        x = np.zeros(n)

    r = b - A@x  # residual; this must be all zeros for feasibility

    A[r < 0] = -A[r < 0]  # express problem with RHS positive for trivial BFS
    b[r < 0] = -b[r < 0]  # to the auxiliary problem
    r[r < 0] *= -1

    # Rows which we will need to find a trivial way to zero.
    # This should just be the rows where there is a nonzero residual.
    # But then we would not necessarily have a column singleton in every row.
    # This makes it difficult to find an initial basis.
    if x0 is None:
        nonzero_constraints = np.arange(m)
    else:
        nonzero_constraints = np.where(r > tol)[0]

    # these are (at least some of) the initial basis columns
    basis = np.where(np.abs(x) > tol)[0]

    if len(nonzero_constraints) == 0 and len(basis) <= m:  # already a BFS
        c = np.zeros(n)
        basis = _get_more_basis_columns(A, basis)
        return A, b, c, basis, x, status
    elif (len(nonzero_constraints) > m - len(basis) or
          np.any(x < 0)):  # can't get trivial BFS
        c = np.zeros(n)
        status = 6
        return A, b, c, basis, x, status

    # chooses existing columns appropriate for inclusion in initial basis
    cols, rows = _select_singleton_columns(A, r)

    # find the rows we need to zero that we _can_ zero with column singletons
    i_tofix = np.isin(rows, nonzero_constraints)
    # these columns can't already be in the basis, though
    # we are going to add them to the basis and change the corresponding x val
    i_notinbasis = np.logical_not(np.isin(cols, basis))
    i_fix_without_aux = np.logical_and(i_tofix, i_notinbasis)
    rows = rows[i_fix_without_aux]
    cols = cols[i_fix_without_aux]

    # indices of the rows we can only zero with auxiliary variable
    # these rows will get a one in each auxiliary column
    arows = nonzero_constraints[np.logical_not(
                                np.isin(nonzero_constraints, rows))]
    n_aux = len(arows)
    acols = n + np.arange(n_aux)          # indices of auxiliary columns

    basis_ng = np.concatenate((cols, acols))   # basis columns not from guess
    basis_ng_rows = np.concatenate((rows, arows))  # rows we need to zero

    # add auxiliary singleton columns
    A = np.hstack((A, np.zeros((m, n_aux))))
    A[arows, acols] = 1

    # generate initial BFS
    x = np.concatenate((x, np.zeros(n_aux)))
    x[basis_ng] = r[basis_ng_rows]/A[basis_ng_rows, basis_ng]

    # generate costs to minimize infeasibility
    c = np.zeros(n_aux + n)
    c[acols] = 1

    # basis columns correspond with nonzeros in guess, those with column
    # singletons we used to zero remaining constraints, and any additional
    # columns to get a full set (m columns)
    basis = np.concatenate((basis, basis_ng))
    basis = _get_more_basis_columns(A, basis)  # add columns as needed

    return A, b, c, basis, x, status

