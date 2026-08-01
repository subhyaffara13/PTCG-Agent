
def optim_inputs_func_sgd(device, dtype=None):
    return [
        OptimizerInput(params=None, kwargs={}, desc="default"),
        OptimizerInput(params=None, kwargs={"lr": 1e-2}, desc="non-default lr"),
        OptimizerInput(
            params=None, kwargs={"lr": torch.tensor(0.001)}, desc="tensor lr"
        ),
        OptimizerInput(
            params=None, kwargs={"weight_decay": 0.5}, desc="non-zero weight_decay"
        ),
        OptimizerInput(params=None, kwargs={"momentum": 0.9}, desc="momentum"),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0.1, "maximize": True},
            desc="maximize",
        ),
        OptimizerInput(
            params=None,
            kwargs={"momentum": 0.9, "dampening": 0.5},
            desc="dampening",
        ),
        OptimizerInput(
            params=None,
            kwargs={"momentum": 0.9, "weight_decay": 0.1},
            desc="weight_decay w/ momentum",
        ),
        OptimizerInput(
            params=None,
            kwargs={"momentum": 0.9, "nesterov": True, "weight_decay": 0.1},
            desc="nesterov",
        ),
    ]

