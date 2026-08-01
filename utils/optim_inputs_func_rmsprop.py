
def optim_inputs_func_rmsprop(device, dtype=None):
    cuda_supported_configs = [
        OptimizerInput(params=None, kwargs={"capturable": True}, desc="capturable"),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0.1, "maximize": True, "capturable": True},
            desc="capturable, maximize",
        ),
        OptimizerInput(
            params=None,
            kwargs={"lr": torch.tensor(0.001), "capturable": True},
            desc="Tensor lr with capturable",
        ),
    ]

    return [
        OptimizerInput(params=None, kwargs={}, desc="default"),
        OptimizerInput(params=None, kwargs={"lr": 1e-3}, desc="non-default lr"),
        OptimizerInput(
            params=None, kwargs={"weight_decay": 0.1}, desc="nonzero weight_decay"
        ),
        OptimizerInput(
            params=None,
            kwargs={
                "maximize": True,
            },
            desc="maximize",
        ),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0.1, "centered": True},
            desc="centered",
        ),
        OptimizerInput(
            params=None,
            kwargs={
                "maximize": True,
                "weight_decay": 0.1,
            },
            desc="maximize, weight_decay",
        ),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0.1, "centered": True, "momentum": 0.1},
            desc="momentum",
        ),
        OptimizerInput(
            params=None,
            kwargs={
                "weight_decay": 0.1,
                "centered": True,
                "momentum": 0.1,
                "maximize": True,
            },
            desc="maximize, centered, weight_decay, w/ momentum",
        ),
    ] + (cuda_supported_configs if _get_device_type(device) in CUDA_CONFIG_GPUS else [])

