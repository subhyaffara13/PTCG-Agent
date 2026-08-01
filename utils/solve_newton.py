
def solve_newton(n, m, h, col_fun, bc, jac, y, p, B, bvp_tol, bc_tol):
    """Solve the nonlinear collocation system by a Newton method.

    This is a simple Newton method with a backtracking line search. As
    advised in [1]_, an affine-invariant criterion function F = ||J^-1 r||^2
    is used, where J is the Jacobian matrix at the current iteration and r is
    the vector or collocation residuals (values of the system lhs).

    The method alters between full Newton iterations and the fixed-Jacobian
    iterations based

    There are other tricks proposed in [1]_, but they are not used as they
    don't seem to improve anything significantly, and even break the
    convergence on some test problems I tried.

    All important parameters of the algorithm are defined inside the function.

    Parameters
    ----------
    n : int
        Number of equations in the ODE system.
    m : int
        Number of nodes in the mesh.
    h : ndarray, shape (m-1,)
        Mesh intervals.
    col_fun : callable
        Function computing collocation residuals.
    bc : callable
        Function computing boundary condition residuals.
    jac : callable
        Function computing the Jacobian of the whole system (including
        collocation and boundary condition residuals). It must return
        scipy.sparse in CSC format ready for use with `scipy.sparse.linalg.splu`.
    y : ndarray, shape (n, m)
        Initial guess for the function values at the mesh nodes.
    p : ndarray, shape (k,)
        Initial guess for the unknown parameters.
    B : ndarray with shape (n, n) or None
        Matrix to force the S y(a) = 0 condition for a problems with the
        singular term. If None, the singular term is assumed to be absent.
    bvp_tol : float
        Tolerance to which we want to solve a BVP.
    bc_tol : float
        Tolerance to which we want to satisfy the boundary conditions.

    Returns
    -------
    y : ndarray, shape (n, m)
        Final iterate for the function values at the mesh nodes.
    p : ndarray, shape (k,)
        Final iterate for the unknown parameters.
    singular : bool
        True, if the LU decomposition failed because Jacobian turned out
        to be singular.

    References
    ----------
    .. [1]  U. Ascher, R. Mattheij and R. Russell "Numerical Solution of
       Boundary Value Problems for Ordinary Differential Equations",
       Philidelphia, PA: Society for Industrial and Applied Mathematics,
       1995.
    """
    # We know that the solution residuals at the middle points of the mesh
    # are connected with collocation residuals  r_middle = 1.5 * col_res / h.
    # As our BVP solver tries to decrease relative residuals below a certain
    # tolerance, it seems reasonable to terminated Newton iterations by
    # comparison of r_middle / (1 + np.abs(f_middle)) with a certain threshold,
    # which we choose to be 1.5 orders lower than the BVP tolerance. We rewrite
    # the condition as col_res < tol_r * (1 + np.abs(f_middle)), then tol_r
    # should be computed as follows:
    tol_r = 2/3 * h * 5e-2 * bvp_tol

    # Maximum allowed number of Jacobian evaluation and factorization, in
    # other words, the maximum number of full Newton iterations. A small value
    # is recommended in the literature.
    max_njev = 4

    # Maximum number of iterations, considering that some of them can be
    # performed with the fixed Jacobian. In theory, such iterations are cheap,
    # but it's not that simple in Python.
    max_iter = 8

    # Minimum relative improvement of the criterion function to accept the
    # step (Armijo constant).
    sigma = 0.2

    # Step size decrease factor for backtracking.
    tau = 0.5

    # Maximum number of backtracking steps, the minimum step is then
    # tau ** n_trial.
    n_trial = 4

    col_res, y_middle, f, f_middle = col_fun(y, p)
    bc_res = bc(y[:, 0], y[:, -1], p)
    res = np.hstack((col_res.ravel(order='F'), bc_res))

    njev = 0
    singular = False
    recompute_jac = True
    for iteration in range(max_iter):
        if recompute_jac:
            J = jac(y, p, y_middle, f, f_middle, bc_res)
            njev += 1
            try:
                LU = splu(J)
            except RuntimeError:
                singular = True
                break

            step = LU.solve(res)
            cost = np.dot(step, step)

        y_step = step[:m * n].reshape((n, m), order='F')
        p_step = step[m * n:]

        alpha = 1
        for trial in range(n_trial + 1):
            y_new = y - alpha * y_step
            if B is not None:
                y_new[:, 0] = np.dot(B, y_new[:, 0])
            p_new = p - alpha * p_step

            col_res, y_middle, f, f_middle = col_fun(y_new, p_new)
            bc_res = bc(y_new[:, 0], y_new[:, -1], p_new)
            res = np.hstack((col_res.ravel(order='F'), bc_res))

            step_new = LU.solve(res)
            cost_new = np.dot(step_new, step_new)
            if cost_new < (1 - 2 * alpha * sigma) * cost:
                break

            if trial < n_trial:
                alpha *= tau

        y = y_new
        p = p_new

        if njev == max_njev:
            break

        if (np.all(np.abs(col_res) < tol_r * (1 + np.abs(f_middle))) and
                np.all(np.abs(bc_res) < bc_tol)):
            break

        # If the full step was taken, then we are going to continue with
        # the same Jacobian. This is the approach of BVP_SOLVER.
        if alpha == 1:
            step = step_new
            cost = cost_new
            recompute_jac = False
        else:
            recompute_jac = True

    return y, p, singular

