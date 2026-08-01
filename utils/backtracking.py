
def backtracking(A, g, x, p, theta, p_dot_g, lb, ub):
    """Find an appropriate step size using backtracking line search."""
    alpha = 1
    while True:
        x_new, _ = reflective_transformation(x + alpha * p, lb, ub)
        step = x_new - x
        cost_change = -evaluate_quadratic(A, g, step)
        if cost_change > -0.1 * alpha * p_dot_g:
            break
        alpha *= 0.5

    active = find_active_constraints(x_new, lb, ub)
    if np.any(active != 0):
        x_new, _ = reflective_transformation(x + theta * alpha * p, lb, ub)
        x_new = make_strictly_feasible(x_new, lb, ub, rstep=0)
        step = x_new - x
        cost_change = -evaluate_quadratic(A, g, step)

    return x, step, cost_change

