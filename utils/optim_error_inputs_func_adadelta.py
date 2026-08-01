
def optim_error_inputs_func_adadelta(device, dtype):
    error_inputs = get_error_inputs_for_all_optims(device, dtype)
    if _get_device_type(device) == "cpu":
        error_inputs += [
            ErrorOptimizerInput(
                OptimizerInput(
                    params=None,
                    kwargs=dict(lr=1e-2, rho=1.1),
                    desc="rho should be between 0 and 1",
                ),
                error_type=ValueError,
                error_regex="Invalid rho value: 1.1",
            ),
        ]
    return error_inputs

