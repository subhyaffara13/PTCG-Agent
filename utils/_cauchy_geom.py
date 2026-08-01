
def _cauchy_geom(const, grad, curv, xl, xu, delta, debug):
    """
    Same as `bound_constrained_cauchy_step` without the absolute value.
    """
    # Calculate the initial active set.
    fixed_xl = (xl < 0.0) & (grad > 0.0)
    fixed_xu = (xu > 0.0) & (grad < 0.0)

    # Calculate the Cauchy step.
    cauchy_step = np.zeros_like(grad)
    cauchy_step[fixed_xl] = xl[fixed_xl]
    cauchy_step[fixed_xu] = xu[fixed_xu]
    if np.linalg.norm(cauchy_step) > delta:
        working = fixed_xl | fixed_xu
        while True:
            # Calculate the Cauchy step for the directions in the working set.
            g_norm = np.linalg.norm(grad[working])
            delta_reduced = np.sqrt(
                delta**2.0 - cauchy_step[~working] @ cauchy_step[~working]
            )
            if g_norm > TINY * abs(delta_reduced):
                mu = max(delta_reduced / g_norm, 0.0)
            else:
                break
            cauchy_step[working] = mu * grad[working]

            # Update the working set.
            fixed_xl = working & (cauchy_step < xl)
            fixed_xu = working & (cauchy_step > xu)
            if not np.any(fixed_xl) and not np.any(fixed_xu):
                # Stop the calculations as the Cauchy step is now feasible.
                break
            cauchy_step[fixed_xl] = xl[fixed_xl]
            cauchy_step[fixed_xu] = xu[fixed_xu]
            working = working & ~(fixed_xl | fixed_xu)

    # Calculate the step that maximizes the quadratic along the Cauchy step.
    grad_step = grad @ cauchy_step
    if grad_step >= 0.0:
        # Set alpha_tr to the step size for the trust-region constraint.
        s_norm = np.linalg.norm(cauchy_step)
        if s_norm > TINY * delta:
            alpha_tr = max(delta / s_norm, 0.0)
        else:
            # The Cauchy step is basically zero.
            alpha_tr = 0.0

        # Set alpha_quad to the step size for the maximization problem.
        curv_step = curv(cauchy_step)
        if curv_step < -TINY * grad_step:
            alpha_quad = max(-grad_step / curv_step, 0.0)
        else:
            alpha_quad = np.inf

        # Set alpha_bd to the step size for the bound constraints.
        i_xl = (xl > -np.inf) & (cauchy_step < TINY * xl)
        i_xu = (xu < np.inf) & (cauchy_step > TINY * xu)
        alpha_xl = np.min(xl[i_xl] / cauchy_step[i_xl], initial=np.inf)
        alpha_xu = np.min(xu[i_xu] / cauchy_step[i_xu], initial=np.inf)
        alpha_bd = min(alpha_xl, alpha_xu)

        # Calculate the solution and the corresponding function value.
        alpha = min(alpha_tr, alpha_quad, alpha_bd)
        step = np.clip(alpha * cauchy_step, xl, xu)
        q_val = const + alpha * grad_step + 0.5 * alpha**2.0 * curv_step
    else:
        # This case is never reached in exact arithmetic. It prevents this
        # function to return a step that decreases the objective function.
        step = np.zeros_like(grad)
        q_val = const

    if debug:
        assert np.all(xl <= step)
        assert np.all(step <= xu)
        assert np.linalg.norm(step) < 1.1 * delta
    return step, q_val

