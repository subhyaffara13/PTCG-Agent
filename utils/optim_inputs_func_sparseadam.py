
def optim_inputs_func_sparseadam(device, dtype=None):
    return [
        OptimizerInput(params=None, kwargs={}, desc="default"),
        OptimizerInput(
            params=None, kwargs={"lr": 0.01}, desc="non-default lr"
        ),  # TODO: Move out to testing in param_group?
        OptimizerInput(
            params=None, kwargs={"lr": torch.tensor(0.001)}, desc="Tensor lr"
        ),
        OptimizerInput(params=None, kwargs={"maximize": True}, desc="maximize"),
    ]

