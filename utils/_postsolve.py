
def _postsolve(x, postsolve_args, complete=False):
    """
    Given solution x to presolved, standard form linear program x, add
    fixed variables back into the problem and undo the variable substitutions
    to get solution to original linear program. Also, calculate the objective
    function value, slack in original upper bound constraints, and residuals
    in original equality constraints.

    Parameters
    ----------
    x : 1-D array
        Solution vector to the standard-form problem.
    postsolve_args : tuple
        Data needed by _postsolve to convert the solution to the standard-form
        problem into the solution to the original problem, including:

    lp : A `scipy.optimize._linprog_util._LPProblem` consisting of the following fields:

        c : 1D array
            The coefficients of the linear objective function to be minimized.
        A_ub : 2D array, optional
            The inequality constraint matrix. Each row of ``A_ub`` specifies the
            coefficients of a linear inequality constraint on ``x``.
        b_ub : 1D array, optional
            The inequality constraint vector. Each element represents an
            upper bound on the corresponding value of ``A_ub @ x``.
        A_eq : 2D array, optional
            The equality constraint matrix. Each row of ``A_eq`` specifies the
            coefficients of a linear equality constraint on ``x``.
        b_eq : 1D array, optional
            The equality constraint vector. Each element of ``A_eq @ x`` must equal
            the corresponding element of ``b_eq``.
        bounds : 2D array
            The bounds of ``x``, lower bounds in the 1st column, upper
            bounds in the 2nd column. The bounds are possibly tightened
            by the presolve procedure.
        x0 : 1D array, optional
            Guess values of the decision variables, which will be refined by
            the optimization algorithm. This argument is currently used only by the
            'revised simplex' method, and can only be used if `x0` represents a
            basic feasible solution.

    revstack: list of functions
        the functions in the list reverse the operations of _presolve()
        the function signature is x_org = f(x_mod), where x_mod is the result
        of a presolve step and x_org the value at the start of the step
    complete : bool
        Whether the solution is was determined in presolve (``True`` if so)

    Returns
    -------
    x : 1-D array
        Solution vector to original linear programming problem
    fun: float
        optimal objective value for original problem
    slack : 1-D array
        The (non-negative) slack in the upper bound constraints, that is,
        ``b_ub - A_ub @ x``
    con : 1-D array
        The (nominally zero) residuals of the equality constraints, that is,
        ``b - A_eq @ x``
    """
    # note that all the inputs are the ORIGINAL, unmodified versions
    # no rows, columns have been removed

    c, A_ub, b_ub, A_eq, b_eq, bounds, x0, integrality = postsolve_args[0]
    revstack, C, b_scale = postsolve_args[1:]

    x = _unscale(x, C, b_scale)

    # Undo variable substitutions of _get_Abc()
    # if "complete", problem was solved in presolve; don't do anything here
    n_x = bounds.shape[0]
    if not complete and bounds is not None:  # bounds are never none, probably
        n_unbounded = 0
        for i, bi in enumerate(bounds):
            lbi = bi[0]
            ubi = bi[1]
            if lbi == -np.inf and ubi == np.inf:
                n_unbounded += 1
                x[i] = x[i] - x[n_x + n_unbounded - 1]
            else:
                if lbi == -np.inf:
                    x[i] = ubi - x[i]
                else:
                    x[i] += lbi
    # all the rest of the variables were artificial
    x = x[:n_x]

    # If there were variables removed from the problem, add them back into the
    # solution vector
    # Apply the functions in revstack (reverse direction)
    for rev in reversed(revstack):
        x = rev(x)

    fun = x.dot(c)
    with np.errstate(invalid="ignore"):
        slack = b_ub - A_ub.dot(x)  # report slack for ORIGINAL UB constraints
        # report residuals of ORIGINAL EQ constraints
        con = b_eq - A_eq.dot(x)

    return x, fun, slack, con

