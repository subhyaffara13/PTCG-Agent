
def optim_inputs_func_adagrad(device, dtype=None):
    return [
        OptimizerInput(params=None, kwargs={}, desc="default"),
        OptimizerInput(
            params=None, kwargs={"weight_decay": 0.1}, desc="nonzero weight_decay"
        ),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0.1, "maximize": True},
            desc="maximize",
        ),
        OptimizerInput(params=None, kwargs={"lr": 0.1}, desc="non-default lr"),
        OptimizerInput(
            params=None,
            kwargs={"initial_accumulator_value": 0.1, "weight_decay": 0.1},
            desc="initial_accumulator_value",
        ),
        OptimizerInput(
            params=None,
            kwargs={"lr": 0.1, "lr_decay": 0.5, "weight_decay": 0.1},
            desc="lr_decay",
        ),  # TODO: Move out to testing in param_group?
        OptimizerInput(
            params=None,
            kwargs={"lr": torch.tensor(0.001)},
            desc="Tensor lr",
        ),
    ]

