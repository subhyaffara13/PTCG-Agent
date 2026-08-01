
def optim_error_inputs_func_muon(device, dtype):
    error_inputs = get_error_inputs_for_all_optims(device, dtype)
    complex_param = torch.rand(2, 3, device=device, dtype=torch.complex64)
    complex_param.grad = torch.rand_like(complex_param)
    non_2d_param = torch.rand(2, 3, 4, device=device, dtype=dtype)
    non_2d_param.grad = torch.rand_like(non_2d_param)
    param = torch.rand(2, 3, device=device, dtype=dtype)
    param.grad = torch.rand_like(param)
    error_inputs += [
        ErrorOptimizerInput(
            OptimizerInput(
                params=[non_2d_param],
                kwargs=dict(),
                desc="only support 2D parameters",
            ),
            error_type=ValueError,
            error_regex="Muon only supports 2D parameters",
            error_on=OptimizerErrorEnum.CONSTRUCTION_ERROR,
        ),
        ErrorOptimizerInput(
            OptimizerInput(
                params=[param],
                kwargs={"adjust_lr_fn": "arbitrary"},
                desc="only support `original` and `match_rms_adamw`",
            ),
            error_type=ValueError,
            error_regex="Adjust learning rate function arbitrary is not supported",
            error_on=OptimizerErrorEnum.CONSTRUCTION_ERROR,
        ),
        ErrorOptimizerInput(
            OptimizerInput(
                params=[complex_param],
                kwargs=dict(),
                desc="does not support complex parameters",
            ),
            error_type=RuntimeError,
            error_regex="Muon does not support complex parameters",
            error_on=OptimizerErrorEnum.STEP_ERROR,
        ),
    ]
    return error_inputs

