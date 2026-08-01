
def _constraints_to_components(constraints):
    """
    Convert sequence of constraints to a single set of components A, b_l, b_u.

    `constraints` could be

    1. A LinearConstraint
    2. A tuple representing a LinearConstraint
    3. An invalid object
    4. A sequence of composed entirely of objects of type 1/2
    5. A sequence containing at least one object of type 3

    We want to accept 1, 2, and 4 and reject 3 and 5.
    """
    message = ("`constraints` (or each element within `constraints`) must be "
               "convertible into an instance of "
               "`scipy.optimize.LinearConstraint`.")
    As = []
    b_ls = []
    b_us = []

    # Accept case 1 by standardizing as case 4
    if isinstance(constraints, LinearConstraint):
        constraints = [constraints]
    else:
        # Reject case 3
        try:
            iter(constraints)
        except TypeError as exc:
            raise ValueError(message) from exc

        # Accept case 2 by standardizing as case 4
        if len(constraints) == 3:
            # argument could be a single tuple representing a LinearConstraint
            try:
                constraints = [LinearConstraint(*constraints)]
            except (TypeError, ValueError, VisibleDeprecationWarning):
                # argument was not a tuple representing a LinearConstraint
                pass

    # Address cases 4/5
    for constraint in constraints:
        # if it's not a LinearConstraint or something that represents a
        # LinearConstraint at this point, it's invalid
        if not isinstance(constraint, LinearConstraint):
            try:
                constraint = LinearConstraint(*constraint)
            except TypeError as exc:
                raise ValueError(message) from exc
        As.append(csc_array(constraint.A))
        b_ls.append(np.atleast_1d(constraint.lb).astype(np.float64))
        b_us.append(np.atleast_1d(constraint.ub).astype(np.float64))

    if len(As) > 1:
        A = vstack(As, format="csc")
        b_l = np.concatenate(b_ls)
        b_u = np.concatenate(b_us)
    else:  # avoid unnecessary copying
        A = As[0]
        b_l = b_ls[0]
        b_u = b_us[0]

    return A, b_l, b_u

