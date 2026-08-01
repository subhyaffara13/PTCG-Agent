
def standardize_constraints(constraints, x0, meth):
    """Converts constraints to the form required by the solver."""
    all_constraint_types = (NonlinearConstraint, LinearConstraint, dict)
    new_constraint_types = all_constraint_types[:-1]
    if constraints is None:
        constraints = []
    elif isinstance(constraints, all_constraint_types):
        constraints = [constraints]
    else:
        constraints = list(constraints)  # ensure it's a mutable sequence

    if meth in ['trust-constr', 'cobyqa', 'new', 'cobyla']:
        for i, con in enumerate(constraints):
            if not isinstance(con, new_constraint_types):
                constraints[i] = old_constraint_to_new(i, con)
    else:
        # iterate over copy, changing original
        for i, con in enumerate(list(constraints)):
            if isinstance(con, new_constraint_types):
                old_constraints = new_constraint_to_old(con, x0)
                constraints[i] = old_constraints[0]
                constraints.extend(old_constraints[1:])  # appends 1 if present

    return constraints

