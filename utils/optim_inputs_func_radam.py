
def optim_inputs_func_radam(device=None, dtype=None):
    cuda_supported_configs = [
        OptimizerInput(params=None, kwargs={"capturable": True}, desc="capturable"),
        OptimizerInput(
            params=None,
            kwargs={
                "capturable": True,
                "weight_decay": 0.1,
            },
            desc="capturable, weight_decay",
        ),
        OptimizerInput(
            params=None,
            kwargs={
                "capturable": True,
                "weight_decay": 0.1,
                "decoupled_weight_decay": True,
            },
            desc="capturable, weight_decay, decoupled_weight_decay",
        ),
        OptimizerInput(
            params=None,
            kwargs={
                "lr": torch.tensor(0.001),
                "capturable": True,
                "weight_decay": 0.1,
                "decoupled_weight_decay": True,
            },
            desc="capturable, weight_decay, decoupled_weight_decay, tensor LR",
        ),
    ]
    return [
        OptimizerInput(params=None, kwargs={}, desc="default"),
        OptimizerInput(params=None, kwargs={"lr": 2e-3}, desc="non-default lr"),
        OptimizerInput(params=None, kwargs={"eps": 1e-6}, desc="non-default eps"),
        OptimizerInput(
            params=None, kwargs={"weight_decay": 0.1}, desc="nonzero weight_decay"
        ),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0.1, "decoupled_weight_decay": True},
            desc="decoupled_weight_decay",
        ),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0.1, "maximize": True},
            desc="maximize",
        ),
    ] + (cuda_supported_configs if _get_device_type(device) in CUDA_CONFIG_GPUS else [])

