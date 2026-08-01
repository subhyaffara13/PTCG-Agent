
def optim_inputs_func_lbfgs(device, dtype=None):
    return [
        OptimizerInput(params=None, kwargs={}, desc="default"),
        OptimizerInput(params=None, kwargs={"lr": 0.01}, desc="non-default lr"),
        OptimizerInput(
            params=None, kwargs={"lr": torch.tensor(0.001)}, desc="Tensor lr"
        ),
        OptimizerInput(
            params=None, kwargs={"tolerance_grad": 1e-6}, desc="tolerance_grad"
        ),
        OptimizerInput(
            params=None,
            kwargs={"line_search_fn": "strong_wolfe"},
            desc="strong_wolfe",
        ),
    ]

