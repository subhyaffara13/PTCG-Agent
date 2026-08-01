
def optim_error_inputs_func_adam(device, dtype):
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
            ErrorOptimizerInput(
                OptimizerInput(
                    params=None,
                    kwargs=dict(lr=torch.tensor(0.001), foreach=True),
                    desc="lr as Tensor doesn't work with foreach & not capturable",
                ),
                error_type=ValueError,
                error_regex="lr as a Tensor is not supported for capturable=False and foreach=True",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=None,
                    kwargs=dict(lr=1e-2, betas=(0.9, torch.tensor(0.99))),
                    desc="betas must be either both floats or both Tensors",
                ),
                error_type=ValueError,
                error_regex="betas must be either both floats or both Tensors",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=None,
                    kwargs=dict(lr=1e-2, betas=(torch.tensor(0.9), 0.99)),
                    desc="betas must be either both floats or both Tensors",
                ),
                error_type=ValueError,
                error_regex="betas must be either both floats or both Tensors",
            ),
            ErrorOptimizerInput(
                OptimizerInput(
                    params=None,
                    kwargs=dict(
                        lr=1e-2,
                        betas=(torch.tensor(0.9), torch.tensor(0.99)),
                        foreach=True,
                    ),
                    desc=r"betas\[0\] as a Tensor is not supported for capturable=False and foreach=True",
                ),
                error_type=ValueError,
                error_regex=r"betas\[0\] as a Tensor is not supported for capturable=False and foreach=True",
            ),
        ]
    if _get_device_type(device) in CUDA_CONFIG_GPUS:
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

