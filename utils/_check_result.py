
def _check_result(x, fun, status, slack, con, bounds, tol, message,
                  integrality):
    """
    Check the validity of the provided solution.

    A valid (optimal) solution satisfies all bounds, all slack variables are
    negative and all equality constraint residuals are strictly non-zero.
    Further, the lower-bounds, upper-bounds, slack and residuals contain
    no nan values.

    Parameters
    ----------
    x : 1-D array
        Solution vector to original linear programming problem
    fun: float
        optimal objective value for original problem
    status : int
        An integer representing the exit status of the optimization::

             0 : Optimization terminated successfully
             1 : Iteration limit reached
             2 : Problem appears to be infeasible
             3 : Problem appears to be unbounded
             4 : Serious numerical difficulties encountered

    slack : 1-D array
        The (non-negative) slack in the upper bound constraints, that is,
        ``b_ub - A_ub @ x``
    con : 1-D array
        The (nominally zero) residuals of the equality constraints, that is,
        ``b - A_eq @ x``
    bounds : 2D array
        The bounds on the original variables ``x``
    message : str
        A string descriptor of the exit status of the optimization.
    tol : float
        Termination tolerance; see [1]_ Section 4.5.

    Returns
    -------
    status : int
        An integer representing the exit status of the optimization::

             0 : Optimization terminated successfully
             1 : Iteration limit reached
             2 : Problem appears to be infeasible
             3 : Problem appears to be unbounded
             4 : Serious numerical difficulties encountered

    message : str
        A string descriptor of the exit status of the optimization.
    """
    # Somewhat arbitrary
    tol = np.sqrt(tol) * 10

    if x is None:
        # HiGHS does not provide x if infeasible/unbounded
        if status == 0:  # Observed with HiGHS Simplex Primal
            status = 4
            message = ("The solver did not provide a solution nor did it "
                       "report a failure. Please submit a bug report.")
        return status, message

    contains_nans = (
        np.isnan(x).any()
        or np.isnan(fun)
        or np.isnan(slack).any()
        or np.isnan(con).any()
    )

    if contains_nans:
        is_feasible = False
    else:
        if integrality is None:
            integrality = 0
        valid_bounds = (x >= bounds[:, 0] - tol) & (x <= bounds[:, 1] + tol)
        # When integrality is 2 or 3, x must be within bounds OR take value 0
        valid_bounds |= (integrality > 1) & np.isclose(x, 0, atol=tol)
        invalid_bounds = not np.all(valid_bounds)

        invalid_slack = status != 3 and (slack < -tol).any()
        invalid_con = status != 3 and (np.abs(con) > tol).any()
        is_feasible = not (invalid_bounds or invalid_slack or invalid_con)

    if status == 0 and not is_feasible:
        status = 4
        message = ("The solution does not satisfy the constraints within the "
                   "required tolerance of " + f"{tol:.2E}" + ", yet "
                   "no errors were raised and there is no certificate of "
                   "infeasibility or unboundedness. Check whether "
                   "the slack and constraint residuals are acceptable; "
                   "if not, consider enabling presolve, adjusting the "
                   "tolerance option(s), and/or using a different method. "
                   "Please consider submitting a bug report.")
    elif status == 2 and is_feasible:
        # Occurs if the simplex method exits after phase one with a very
        # nearly basic feasible solution. Postsolving can make the solution
        # basic, however, this solution is NOT optimal
        status = 4
        message = ("The solution is feasible, but the solver did not report "
                   "that the solution was optimal. Please try a different "
                   "method.")

    return status, message

