
def optim_error_inputs_func_adafactor(device, dtype):
    error_inputs = get_error_inputs_for_all_optims(device, dtype)
    if _get_device_type(device) == "cpu":
        complex_param = torch.rand(2, 3, device=device, dtype=torch.complex64)
        complex_param.grad = torch.rand_like(complex_param)
        error_inputs += [
            ErrorOptimizerInput(
                OptimizerInput(
                    params=None,
                    kwargs=dict(eps=(-1e-30, 1e-3)),
                    desc="epsilon1 should be >= 0",
                ),
                error_type=ValueError,
                error_regex="epsilon1 should be >= 0",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=None,
                    kwargs=dict(d=0.0),
                    desc="invalid d",
                ),
                error_type=ValueError,
                error_regex="Clipping threshold d should be >= 1",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=None,
                    kwargs=dict(beta2_decay=0.8),
                    desc="invalid beta2_decay",
                ),
                error_type=ValueError,
                error_regex="beta2_decay should be <= 0",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=[complex_param],
                    kwargs=dict(),
                    desc="does not support complex parameters",
                ),
                error_type=RuntimeError,
                error_regex="Adafactor does not support complex parameters",
                error_on=OptimizerErrorEnum.STEP_ERROR,
            ),
        ]
    return error_inputs

