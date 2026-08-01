
def optim_inputs_func_adafactor(device, dtype=None):
    return [
        OptimizerInput(params=None, kwargs={}, desc="default"),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0.1, "lr": 0.01},
            desc="nonzero weight_decay",
        ),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0.1, "maximize": True},
            desc="maximize",
        ),
        OptimizerInput(
            params=None,
            kwargs={"beta2_decay": -1.0},
            desc="non-default beta2_decay",
        ),
        OptimizerInput(
            params=None,
            kwargs={"d": 1.5},
            desc="non-default clipping threshold d",
        ),
    ]

