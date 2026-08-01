
def _get_constraints(constraints):
    """
    Extract the linear and nonlinear constraints.
    """
    if isinstance(constraints, dict) or not hasattr(constraints, "__len__"):
        constraints = (constraints,)

    # Extract the linear and nonlinear constraints.
    linear_constraints = []
    nonlinear_constraints = []
    for constraint in constraints:
        if isinstance(constraint, LinearConstraint):
            lb = exact_1d_array(
                constraint.lb,
                "The lower bound of the linear constraints must be a vector.",
            )
            ub = exact_1d_array(
                constraint.ub,
                "The upper bound of the linear constraints must be a vector.",
            )
            linear_constraints.append(
                LinearConstraint(
                    constraint.A,
                    *np.broadcast_arrays(lb, ub),
                )
            )
        elif isinstance(constraint, NonlinearConstraint):
            lb = exact_1d_array(
                constraint.lb,
                "The lower bound of the "
                "nonlinear constraints must be a "
                "vector.",
            )
            ub = exact_1d_array(
                constraint.ub,
                "The upper bound of the "
                "nonlinear constraints must be a "
                "vector.",
            )
            nonlinear_constraints.append(
                NonlinearConstraint(
                    constraint.fun,
                    *np.broadcast_arrays(lb, ub),
                )
            )
        elif isinstance(constraint, dict):
            if "type" not in constraint or constraint["type"] not in (
                "eq",
                "ineq",
            ):
                raise ValueError('The constraint type must be "eq" or "ineq".')
            if "fun" not in constraint or not callable(constraint["fun"]):
                raise ValueError("The constraint function must be callable.")
            nonlinear_constraints.append(
                {
                    "fun": constraint["fun"],
                    "type": constraint["type"],
                    "args": constraint.get("args", ()),
                }
            )
        else:
            raise TypeError(
                "The constraints must be instances of "
                "scipy.optimize.LinearConstraint, "
                "scipy.optimize.NonlinearConstraint, or dict."
            )
    return linear_constraints, nonlinear_constraints

