
def _optimize_result_for_equal_bounds(
        fun, bounds, method, args=(), constraints=()
):
    """
    Provides a default OptimizeResult for when a bounded minimization method
    has (lb == ub).all().

    Parameters
    ----------
    fun: callable
    bounds: Bounds
    method: str
    constraints: Constraint
    """
    success = True
    message = 'All independent variables were fixed by bounds.'

    # bounds is new-style
    x0 = bounds.lb

    if constraints:
        message = ("All independent variables were fixed by bounds at values"
                   " that satisfy the constraints.")
        constraints = standardize_constraints(constraints, x0, 'new')

    maxcv = 0
    for c in constraints:
        pc = PreparedConstraint(c, x0)
        violation = pc.violation(x0)
        if np.sum(violation):
            maxcv = max(maxcv, np.max(violation))
            success = False
            message = (f"All independent variables were fixed by bounds, but "
                       f"the independent variables do not satisfy the "
                       f"constraints exactly. (Maximum violation: {maxcv}).")

    return OptimizeResult(
        x=x0, fun=fun(x0, *args), success=success, message=message, nfev=1,
        njev=0, nhev=0,
    )

