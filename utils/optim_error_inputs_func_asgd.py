
def optim_error_inputs_func_asgd(device, dtype):
    error_inputs = get_error_inputs_for_all_optims(device, dtype)
    if _get_device_type(device) == "cpu":
        error_inputs += [
            ErrorOptimizerInput(
                OptimizerInput(
                    params=None,
                    kwargs=dict(lr=1e-2, weight_decay=-0.5),
                    desc="weight_decay should > 0",
                ),
                error_type=ValueError,
                error_regex="Invalid weight_decay value: -0.5",
            ),
        ]
    return error_inputs

