
def optim_error_inputs_func_adagrad(device, dtype):
    error_inputs = get_error_inputs_for_all_optims(device, dtype)
    if _get_device_type(device) == "cpu":
        error_inputs += [
            ErrorOptimizerInput(
                OptimizerInput(
                    params=None,
                    kwargs=dict(lr=1e-2, lr_decay=-0.5),
                    desc="lr_decay must be bigger than 0",
                ),
                error_type=ValueError,
                error_regex="Invalid lr_decay value: -0.5",
            ),
        ]
    if _get_device_type(device) == "cuda":
        sample_tensor = torch.empty((), device=device, dtype=dtype)
        error_inputs += [
            ErrorOptimizerInput(
                OptimizerInput(
                    params=[sample_tensor],
                    kwargs={"foreach": True, "fused": True},
                    desc="`fused` and `foreach` cannot be `True` together",
                ),
                error_type=RuntimeError,
                error_regex="`fused` and `foreach` cannot be `True` together",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=[sample_tensor],
                    kwargs={"fused": True, "differentiable": True},
                    desc="`fused` does not support `differentiable`",
                ),
                error_type=RuntimeError,
                error_regex="`fused` does not support `differentiable`",
            ),
        ]
    return error_inputs

