
def optim_inputs_func_adamax(device, dtype=None):
    cuda_supported_configs = [
        OptimizerInput(params=None, kwargs={"capturable": True}, desc="capturable"),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0.9, "maximize": True, "capturable": True},
            desc="capturable, maximize, weight_decay",
        ),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0, "maximize": True, "capturable": True},
            desc="capturable, maximize",
        ),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0.9, "maximize": False, "capturable": True},
            desc="capturable, weight_decay",
        ),
        OptimizerInput(
            params=None,
            kwargs={
                "lr": torch.tensor(0.001),
                "weight_decay": 0.9,
                "maximize": False,
                "capturable": True,
            },
            desc="capturable, weight_decay, tensor LR",
        ),
    ]

    return [
        OptimizerInput(params=None, kwargs={}, desc="default"),
        OptimizerInput(params=None, kwargs={"lr": 0.1}, desc="non-default lr"),
        OptimizerInput(
            params=None, kwargs={"weight_decay": 0.1}, desc="nonzero weight_decay"
        ),
        OptimizerInput(
            params=None,
            kwargs={"maximize": True},
            desc="maximize",
        ),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0.1, "maximize": True},
            desc="maximize, weight_decay",
        ),
    ] + (cuda_supported_configs if _get_device_type(device) in CUDA_CONFIG_GPUS else [])

