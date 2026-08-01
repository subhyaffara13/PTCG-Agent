
def optim_error_inputs_func_radam(device, dtype):
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
                    params=None,
                    kwargs=dict(lr=1e-2, weight_decay=-1),
                    desc="weight_decay should > 0",
                ),
                error_type=ValueError,
                error_regex="Invalid weight_decay value: -1",
            ),
        ]
    return error_inputs

