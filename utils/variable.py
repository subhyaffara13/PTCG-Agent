
def variable(*args, **kwargs):  # noqa: D103
    raise RuntimeError(
        "torch.autograd.variable(...) is deprecated, use torch.tensor(...) instead"
    )

