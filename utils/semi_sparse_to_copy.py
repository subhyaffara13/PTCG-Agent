
def semi_sparse_to_copy(func, types, args, kwargs=None) -> torch.Tensor:
    self = args[0]
    kwargs = kwargs or {}

    device = kwargs.get("device", None)

    if device is not None and torch.device(device).type == "cpu":
        dense = self.to_dense()
        return func(dense, **kwargs)

    raise NotImplementedError(
        f"`_to_copy()` with kwargs={kwargs} is not implemented "
        "for SparseSemiStructuredTensor. Only converting to CPU is supported currently."
    )

