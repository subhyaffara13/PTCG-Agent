
def optim_error_inputs_func_rprop(device, dtype):
    error_inputs = get_error_inputs_for_all_optims(device, dtype)
    if _get_device_type(device) == "cpu":
        error_inputs += [
            ErrorOptimizerInput(
                OptimizerInput(
                    params=None,
                    kwargs=dict(lr=1e-2, etas=(1.0, 0.5)),
                    desc="0 < eta1 < 1 < eta2",
                ),
                error_type=ValueError,
                error_regex="Invalid eta values: 1.0, 0.5",
            ),
        ]
    return error_inputs

