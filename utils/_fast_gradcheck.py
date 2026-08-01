
def _fast_gradcheck(
    func,
    func_out,
    inputs,
    outputs,
    eps,
    rtol,
    atol,
    check_grad_dtypes,
    nondet_tol,
    *,
    use_forward_ad=False,
    complex_indices=None,
    test_imag=False,
    masked=False,
):
    # See https://github.com/pytorch/pytorch/issues/53876 for details
    inp_tensors_idx, inp_tensors = _get_inp_tensors(inputs)
    # Backward mode computes v^T * J (VJP)
    # Since we computed J * u (JVP) through finite difference method, we perform an equality check
    # between VJP * u, v * JVP
    # ----
    # Forward mode computes J * u (JVP)
    # Since we already compute JVP through finite difference method,
    # we don't need v for correctness check here as asserted below
    all_v, all_u, all_u_dense = _make_vectors(
        inp_tensors, outputs, use_forward_ad=use_forward_ad
    )

    inputs_numerical, all_u_numerical, all_v_numerical = (
        (inputs, all_u, all_v) if masked else _densify((inputs, all_u, all_v))
    )

    numerical_vJu = _get_numerical_vJu(
        func,
        inputs_numerical,
        inp_tensors_idx,
        func_out,
        all_u_numerical,
        all_v_numerical,
        eps,
        is_forward_ad=use_forward_ad,
    )
    # TODO: replicate https://github.com/pytorch/pytorch/pull/77743 for fast gradcheck as well
    if use_forward_ad:
        if all_v is not None:
            raise AssertionError("Expected all_v to be None.")
        analytical_vJu = _get_analytical_jacobian_forward_ad(
            func,
            inputs,
            _as_tuple(func_out),
            all_u=all_u,
            check_grad_dtypes=check_grad_dtypes,
        )
    else:
        if not outputs:
            _check_no_differentiable_outputs_fast(
                func, func_out, inputs, inp_tensors_idx, all_u, eps, nondet_tol
            )

        analytical_vJu = _get_analytical_vJu_backward_mode(
            inputs, outputs, nondet_tol, check_grad_dtypes, all_v, all_u_dense
        )

    _check_analytical_numerical_equal(
        analytical_vJu,
        numerical_vJu,
        complex_indices,
        inputs,
        outputs,
        func,
        all_v,
        all_u,
        rtol,
        atol,
        eps,
        test_imag,
        is_forward_ad=use_forward_ad,
    )

    return True

