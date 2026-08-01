
def _phase_two(c, A, x, b, callback, postsolve_args, maxiter, tol, disp,
               maxupdate, mast, pivot, iteration=0, phase_one_n=None):
    """
    The heart of the simplex method. Beginning with a basic feasible solution,
    moves to adjacent basic feasible solutions successively lower reduced cost.
    Terminates when there are no basic feasible solutions with lower reduced
    cost or if the problem is determined to be unbounded.

    This implementation follows the revised simplex method based on LU
    decomposition. Rather than maintaining a tableau or an inverse of the
    basis matrix, we keep a factorization of the basis matrix that allows
    efficient solution of linear systems while avoiding stability issues
    associated with inverted matrices.
    """
    m, n = A.shape
    status = 0
    a = np.arange(n)                    # indices of columns of A
    ab = np.arange(m)                   # indices of columns of B
    if maxupdate:
        # basis matrix factorization object; similar to B = A[:, b]
        B = BGLU(A, b, maxupdate, mast)
    else:
        B = LU(A, b)

    for iteration in range(iteration, maxiter):

        if disp or callback is not None:
            _display_and_callback(phase_one_n, x, postsolve_args, status,
                                  iteration, disp, callback)

        bl = np.zeros(len(a), dtype=bool)
        bl[b] = 1

        xb = x[b]       # basic variables
        cb = c[b]       # basic costs

        try:
            v = B.solve(cb, transposed=True)    # similar to v = solve(B.T, cb)
        except LinAlgError:
            status = 4
            break

        # TODO: cythonize?
        c_hat = c - v.dot(A)    # reduced cost
        c_hat = c_hat[~bl]
        # Above is much faster than:
        # N = A[:, ~bl]                 # slow!
        # c_hat = c[~bl] - v.T.dot(N)
        # Can we perform the multiplication only on the nonbasic columns?

        if np.all(c_hat >= -tol):  # all reduced costs positive -> terminate
            break

        j = _select_enter_pivot(c_hat, bl, a, rule=pivot, tol=tol)
        u = B.solve(A[:, j])        # similar to u = solve(B, A[:, j])

        i = u > tol                 # if none of the u are positive, unbounded
        if not np.any(i):
            status = 3
            break

        th = xb[i]/u[i]
        l = np.argmin(th)           # implicitly selects smallest subscript
        th_star = th[l]             # step size

        x[b] = x[b] - th_star*u     # take step
        x[j] = th_star
        B.update(ab[i][l], j)       # modify basis
        b = B.b                     # similar to b[ab[i][l]] =

    else:
        # If the end of the for loop is reached (without a break statement),
        # then another step has been taken, so the iteration counter should
        # increment, info should be displayed, and callback should be called.
        iteration += 1
        status = 1
        if disp or callback is not None:
            _display_and_callback(phase_one_n, x, postsolve_args, status,
                                  iteration, disp, callback)

    return x, b, status, iteration

