
def optim_inputs_func_muon(device, dtype=None):
    return [
        OptimizerInput(params=None, kwargs={}, desc="default"),
        OptimizerInput(params=None, kwargs={"lr": 0.01}, desc="non-default lr"),
        OptimizerInput(
            params=None, kwargs={"lr": torch.tensor(0.001)}, desc="Tensor lr"
        ),
        OptimizerInput(
            params=None,
            kwargs={"weight_decay": 0.2},
            desc="non-default weight_decay",
        ),
        OptimizerInput(
            params=None,
            kwargs={"momentum": 0.8},
            desc="non-default momentum",
        ),
        OptimizerInput(
            params=None,
            kwargs={"ns_steps": 6},
            desc="passing alternative ns_steps",
        ),
        OptimizerInput(
            params=None,
            kwargs={
                "ns_coefficients": (3.4, -4.7, 2.0),
            },
            desc="passing alternative ns_coefficients",
        ),
    ]

