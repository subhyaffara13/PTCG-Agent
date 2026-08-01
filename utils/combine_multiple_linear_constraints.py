
def combine_multiple_linear_constraints(constraints):
    full_A = constraints[0].A
    full_lb = constraints[0].lb
    full_ub = constraints[0].ub
    for constraint in constraints[1:]:
        full_A = np.concatenate((full_A, constraint.A), axis=0)
        full_lb = np.concatenate((full_lb, constraint.lb), axis=0)
        full_ub = np.concatenate((full_ub, constraint.ub), axis=0)
    return LinearConstraint(full_A, full_lb, full_ub)

