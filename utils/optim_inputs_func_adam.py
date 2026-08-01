
def optim_inputs_func_adam(device, dtype=None):
    cuda_supported_configs = [
        OptimizerInput(params=None, kwargs={"capturable": True}, desc="capturable"),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0.1, "amsgrad": True, "capturable": True},
            desc="capturable, amsgrad",
        ),
        OptimizerInput(
            params=None,
            kwargs={"lr": torch.tensor(0.001), "amsgrad": True, "capturable": True},
            desc="Tensor lr with capturable and amsgrad",
        ),
        OptimizerInput(
            params=None,
            kwargs={
                "lr": torch.tensor(0.001),
                "betas": (torch.tensor([[[0.9]]]), torch.tensor([[0.99]])),
                "amsgrad": True,
                "capturable": True,
            },
            desc="Tensor lr, Tensor betas, with capturable and amsgrad",
        ),
        OptimizerInput(
            params=None,
            kwargs={
                "lr": torch.tensor(0.001),
                "betas": (torch.tensor(0.9), torch.tensor(0.99)),
                "amsgrad": False,
                "capturable": True,
            },
            desc="Tensor lr, Tensor betas, with capturable",
        ),
    ]
    mps_supported_configs = [
        OptimizerInput(
            params=None, kwargs={"lr": torch.tensor(0.01)}, desc="Tensor lr"
        ),
    ]

    total = (
        [
            OptimizerInput(params=None, kwargs={}, desc="default"),
            OptimizerInput(params=None, kwargs={"lr": 0.01}, desc="non-default lr"),
            OptimizerInput(
                params=None, kwargs={"weight_decay": 0.1}, desc="nonzero weight_decay"
            ),
            OptimizerInput(
                params=None,
                kwargs={"weight_decay": 0.1, "maximize": True},
                desc="maximize",
            ),
            OptimizerInput(
                params=None,
                kwargs={"weight_decay": 0.1, "amsgrad": True},
                desc="amsgrad",
            ),
        ]
        + (
            cuda_supported_configs
            if _get_device_type(device) in CUDA_CONFIG_GPUS
            else []
        )
        + (mps_supported_configs if _get_device_type(device) == "mps" else [])
    )
    if dtype == torch.float16:
        for input in total:
            """
            Too small eps will make denom to be zero for low precision dtype
            denom = (exp_avg_sq.sqrt() / bias_correction2_sqrt).add_(eps)
            For example,
            >>> a
            tensor([0.], dtype=torch.float16)
            >>> a + 1e-8
            tensor([0.], dtype=torch.float16)
            """
            input.kwargs["eps"] = 0.1
    return total

