
def optim_error_inputs_func_sparseadam(device, dtype):
    error_inputs = get_error_inputs_for_all_optims(device, dtype)

    if _get_device_type(device) == "cpu":
        error_inputs += [
            ErrorOptimizerInput(
                OptimizerInput(
                    params=None,
                    kwargs=dict(lr=1e-2, betas=(1.0, 0.0)),
                    desc="beta1 should be between 0 and 1",
                ),
                error_type=ValueError,
                error_regex="Invalid beta parameter at index 0: 1.0",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=[
                        torch.zeros(
                            3, layout=torch.sparse_coo, device=device, dtype=dtype
                        )
                    ],
                    kwargs={},
                    desc="dense params required",
                ),
                error_type=ValueError,
                error_regex="SparseAdam requires dense parameter tensors",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=[
                        {
                            "params": [
                                torch.zeros(
                                    3,
                                    layout=torch.sparse_coo,
                                    device=device,
                                    dtype=dtype,
                                )
                            ]
                        }
                    ],
                    kwargs={},
                    desc="dense params required in param_groups",
                ),
                error_type=ValueError,
                error_regex="SparseAdam requires dense parameter tensors",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=[torch.rand(2, 3, device=device, dtype=torch.complex64)],
                    kwargs={},
                    desc="complex not supported",
                ),
                error_type=ValueError,
                error_regex="SparseAdam does not support complex parameters",
            ),
        ]
    return error_inputs

