
def _run_slow_mode_and_get_error(
    func, tupled_inputs, outputs, input_idx, output_idx, rtol, atol, eps, is_forward_ad
):
    # Compute jacobians in slow mode for better error message
    slow_numerical = _get_numerical_jacobian(
        func, tupled_inputs, outputs, eps=eps, is_forward_ad=is_forward_ad
    )[input_idx][output_idx]
    if is_forward_ad:

        def new_fn(inp):
            new_inputs = list(tupled_inputs)
            new_inputs[input_idx] = inp
            return _as_tuple(func(*new_inputs))[output_idx]

        slow_analytical = _get_analytical_jacobian_forward_ad(
            new_fn, (tupled_inputs[input_idx],), (outputs[output_idx],)
        )[0][0]
    else:
        slow_analytical = _get_analytical_jacobian(
            tupled_inputs, outputs, input_idx, output_idx
        )

    # Assume jacobians are non-empty and have the same shape
    slow_max_diff = (slow_numerical - slow_analytical).abs().max()

    slow_allclose = torch.allclose(slow_analytical, slow_numerical, rtol, atol)
    msg = (
        "\nThe above quantities relating the numerical and analytical jacobians are computed \n"
        "in fast mode. See: https://github.com/pytorch/pytorch/issues/53876 for more background \n"
        "about fast mode. Below, we recompute numerical and analytical jacobians in slow mode:\n\n"
        f"Numerical:\n {slow_numerical}\n"
        f"Analytical:\n{slow_analytical}\n\n"
        f"The max per-element difference (slow mode) is: {slow_max_diff}.\n"
    )
    if slow_allclose:
        # Slow gradcheck would've passed!
        msg += FAST_FAIL_SLOW_OK_MSG
    return msg

