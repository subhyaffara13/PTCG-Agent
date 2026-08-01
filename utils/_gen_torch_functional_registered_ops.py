
def _gen_torch_functional_registered_ops():
    # eventually ops should encompass all of torch/functional.py, (torch.functional.__all__)
    # but we are currently only able to compile some of the functions. additionally,
    # some functions directly map to their aten:: implementations.
    # TODO: add support for more ops
    ops = [
        "stft",
        "istft",
        "lu",
        "cdist",
        "norm",
        "unique",
        "unique_consecutive",
        "tensordot",
    ]
    return {getattr(torch.functional, name) for name in ops}

