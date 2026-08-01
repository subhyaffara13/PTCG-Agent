
def select_step(x, J_h, diag_h, g_h, p, p_h, d, Delta, lb, ub, theta):
    """Select the best step according to Trust Region Reflective algorithm."""
    if in_bounds(x + p, lb, ub):
        p_value = evaluate_quadratic(J_h, g_h, p_h, diag=diag_h)
        return p, p_h, -p_value

    p_stride, hits = step_size_to_bound(x, p, lb, ub)

    # Compute the reflected direction.
    r_h = np.copy(p_h)
    r_h[hits.astype(bool)] *= -1
    r = d * r_h

    # Restrict trust-region step, such that it hits the bound.
    p *= p_stride
    p_h *= p_stride
    x_on_bound = x + p

    # Reflected direction will cross first either feasible region or trust
    # region boundary.
    _, to_tr = intersect_trust_region(p_h, r_h, Delta)
    to_bound, _ = step_size_to_bound(x_on_bound, r, lb, ub)

    # Find lower and upper bounds on a step size along the reflected
    # direction, considering the strict feasibility requirement. There is no
    # single correct way to do that, the chosen approach seems to work best
    # on test problems.
    r_stride = min(to_bound, to_tr)
    if r_stride > 0:
        r_stride_l = (1 - theta) * p_stride / r_stride
        if r_stride == to_bound:
            r_stride_u = theta * to_bound
        else:
            r_stride_u = to_tr
    else:
        r_stride_l = 0
        r_stride_u = -1

    # Check if reflection step is available.
    if r_stride_l <= r_stride_u:
        a, b, c = build_quadratic_1d(J_h, g_h, r_h, s0=p_h, diag=diag_h)
        r_stride, r_value = minimize_quadratic_1d(
            a, b, r_stride_l, r_stride_u, c=c)
        r_h *= r_stride
        r_h += p_h
        r = r_h * d
    else:
        r_value = np.inf

    # Now correct p_h to make it strictly interior.
    p *= theta
    p_h *= theta
    p_value = evaluate_quadratic(J_h, g_h, p_h, diag=diag_h)

    ag_h = -g_h
    ag = d * ag_h

    to_tr = Delta / norm(ag_h)
    to_bound, _ = step_size_to_bound(x, ag, lb, ub)
    if to_bound < to_tr:
        ag_stride = theta * to_bound
    else:
        ag_stride = to_tr

    a, b = build_quadratic_1d(J_h, g_h, ag_h, diag=diag_h)
    ag_stride, ag_value = minimize_quadratic_1d(a, b, 0, ag_stride)
    ag_h *= ag_stride
    ag *= ag_stride

    if p_value < r_value and p_value < ag_value:
        return p, p_h, -p_value
    elif r_value < p_value and r_value < ag_value:
        return r, r_h, -r_value
    else:
        return ag, ag_h, -ag_value


def select_step(x, A_h, g_h, c_h, p, p_h, d, lb, ub, theta):
    """Select the best step according to Trust Region Reflective algorithm."""
    if in_bounds(x + p, lb, ub):
        return p

    p_stride, hits = step_size_to_bound(x, p, lb, ub)
    r_h = np.copy(p_h)
    r_h[hits.astype(bool)] *= -1
    r = d * r_h

    # Restrict step, such that it hits the bound.
    p *= p_stride
    p_h *= p_stride
    x_on_bound = x + p

    # Find the step size along reflected direction.
    r_stride_u, _ = step_size_to_bound(x_on_bound, r, lb, ub)

    # Stay interior.
    r_stride_l = (1 - theta) * r_stride_u
    r_stride_u *= theta

    if r_stride_u > 0:
        a, b, c = build_quadratic_1d(A_h, g_h, r_h, s0=p_h, diag=c_h)
        r_stride, r_value = minimize_quadratic_1d(
            a, b, r_stride_l, r_stride_u, c=c)
        r_h = p_h + r_h * r_stride
        r = d * r_h
    else:
        r_value = np.inf

    # Now correct p_h to make it strictly interior.
    p_h *= theta
    p *= theta
    p_value = evaluate_quadratic(A_h, g_h, p_h, diag=c_h)

    ag_h = -g_h
    ag = d * ag_h
    ag_stride_u, _ = step_size_to_bound(x, ag, lb, ub)
    ag_stride_u *= theta
    a, b = build_quadratic_1d(A_h, g_h, ag_h, diag=c_h)
    ag_stride, ag_value = minimize_quadratic_1d(a, b, 0, ag_stride_u)
    ag *= ag_stride

    if p_value < r_value and p_value < ag_value:
        return p
    elif r_value < p_value and r_value < ag_value:
        return r
    else:
        return ag


def select_step(v1, v2, nv, hour=False, include_last=True,
                threshold_factor=3600.):

    if v1 > v2:
        v1, v2 = v2, v1

    dv = (v2 - v1) / nv

    if hour:
        _select_step = select_step_hour
        cycle = 24.
    else:
        _select_step = select_step_degree
        cycle = 360.

    # for degree
    if dv > 1 / threshold_factor:
        step, factor = _select_step(dv)
    else:
        step, factor = select_step_sub(dv*threshold_factor)

        factor = factor * threshold_factor

    levs = np.arange(np.floor(v1 * factor / step),
                     np.ceil(v2 * factor / step) + 0.5,
                     dtype=int) * step

    # n : number of valid levels. If there is a cycle, e.g., [0, 90, 180,
    # 270, 360], the grid line needs to be extended from 0 to 360, so
    # we need to return the whole array. However, the last level (360)
    # needs to be ignored often. In this case, so we return n=4.

    n = len(levs)

    # we need to check the range of values
    # for example, -90 to 90, 0 to 360,

    if factor == 1. and levs[-1] >= levs[0] + cycle:  # check for cycle
        nv = int(cycle / step)
        if include_last:
            levs = levs[0] + np.arange(0, nv+1, 1) * step
        else:
            levs = levs[0] + np.arange(0, nv, 1) * step

        n = len(levs)

    return np.array(levs), n, factor

