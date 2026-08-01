
def _adjusted_atol(atol, u, v):
    # In slow gradcheck, we compare A and B element-wise, i.e., for some a, b we
    # allow: |a - b| < atol + rtol * b. But since we now compare q1 = v^T A u and
    # q2 = v^T B u, we must allow |q1 - q2| < v^T E u + rtol * v^T B u, where E is
    # the correctly sized matrix in which each entry is atol.
    #
    # We see that atol needs to be scaled by v^T M u (where M is an all-ones M x N
    # matrix): v^T M u = \sum_{i} \sum_{j} u[i] * v[j] = sum(u) * sum(v).

    # For the case of complex inputs, u has re and im. components: u = (ur, ui).
    # Let q = a - b = (qr, qi) in the above notation, eg. q is the difference between analytic and numerical
    # Jacobians. Then the transformed tolerance checks being done in the torch.allclose ops
    # are of form abs(Re{q_r u_r - q_i u_i}) < atol * (abs(u_r) + abs(u_i)), and equivalently
    # for imaginary components abs(Im{q_r u_r - q_i ui}) < atol * (abs(u_r) + abs(u_i)).
    # Since u is drawn randomly non-negative, the end effect is a factor
    # (sum(u_r) + sum(u_i)) * sum(v) increase in atol for complex inputs, eg.
    # a statistical factor of 2 as compared to the real case.

    sum_v = 1.0 if v is None else v.sum()

    if isinstance(u, tuple):
        # case of complex input
        ur, ui = u[0], u[1]
        sum_ur = ur.sum()
        sum_ui = ui.sum()
        complex_modified_atol = atol * (float(sum_ur) + float(sum_ui)) * float(sum_v)
        return complex_modified_atol

    # case of real input
    sum_u = u.sum()
    modified_atol = atol * float(sum_u) * float(sum_v)
    return modified_atol

