
def _reflection_or_replication_pad(
    a: Tensor,
    padding: tuple[int, ...],
    idx_fn: Callable[[int, int, int], Tensor],
) -> Tensor:
    dim = len(padding) // 2
    torch._check(
        a.dim() in (dim + 1, dim + 2),
        lambda: f"reflection_pad{dim}d requires {dim + 1}D or {dim + 2}D input",
    )
    inp_shape = a.shape[-dim:]
    nc_dim = a.dim() - dim

    padding_left = [padding[2 * (dim - 1 - i)] for i in range(dim)]
    padding_right = [padding[2 * (dim - 1 - i) + 1] for i in range(dim)]

    result = a
    for i in range(dim):
        idx: list[Any] = [None] * result.dim()
        idx[i + nc_dim] = idx_fn(padding_left[i], inp_shape[i], padding_right[i])
        result = aten._unsafe_index(result, idx)

    # convert output to correct memory format, if necessary
    memory_format = utils.suggest_memory_format(result)
    result = result.contiguous(memory_format=memory_format)
    return result

