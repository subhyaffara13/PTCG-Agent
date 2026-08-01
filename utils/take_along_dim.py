
def take_along_dim(
    a: torch.Tensor, indices: torch.Tensor, dim: int | None = None
) -> torch.Tensor:
    torch._check(
        a.ndim == indices.ndim,
        lambda: (
            "torch.take_along_dim(): input and indices should have the same "
            f"number of dimensions, but got {a.ndim} dimensions for input, and "
            f"{indices.ndim} dimensions for indices"
        ),
    )

    torch._check(
        utils.is_integer_dtype(indices.dtype),
        lambda: (
            "torch.take_along_dim(): dtype of indices should be int but got "
            f"{indices.dtype} instead"
        ),
    )

    if dim is None:
        return torch.gather(a.view(-1), 0, indices.view(-1))
    else:
        self_sizes = list(a.shape)
        self_sizes[dim] = indices.size(dim)
        broadcast_shape = utils.infer_size_shapes(self_sizes, indices.size())
        indices_broadcast = broadcast_to(indices, broadcast_shape)

        indices_sizes = list(indices.shape)
        indices_sizes[dim] = a.size(dim)
        broadcast_shape = utils.infer_size_shapes(indices_sizes, a.size())
        self_broadcast = broadcast_to(a, broadcast_shape)

        # wrap negative indices
        dim_size = self_broadcast.size(dim)
        indices_broadcast = indices_broadcast % dim_size

        return torch.gather(self_broadcast, dim, indices_broadcast)

