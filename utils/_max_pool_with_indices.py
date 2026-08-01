
def _max_pool_with_indices(
    x: torch.Tensor,
    kernel_size: list[int],
    stride: int | list[int] | None,
    padding: int | list[int],
    dilation: int | list[int],
    ceil_mode: bool,
    dim: int,
) -> tuple[torch.Tensor, torch.Tensor]:
    if dilation == 1:
        dilation = [1] * dim

    if padding == 0:
        padding = [0] * dim

    if not stride:
        stride = kernel_size

    # pyrefly: ignore [bad-assignment]
    kernel_size = pad_listlike(kernel_size, dim)
    # pyrefly: ignore [bad-assignment]
    dilation = pad_listlike(dilation, dim)
    # pyrefly: ignore [bad-assignment]
    padding = pad_listlike(padding, dim)
    # pyrefly: ignore [bad-assignment]
    stride = pad_listlike(stride, dim)

    window_size = functools.reduce(operator.mul, kernel_size)
    # We fallback when using non-default dilation or when the window size is too large
    if (
        torch._inductor.lowering.should_fallback_max_pool_with_indices(
            kernel_size, n_dim=dim
        )
        or window_size > torch.iinfo(torch.int8).max
    ):
        return NotImplemented

    vals, offsets = prims._low_memory_max_pool_with_offsets(
        x,
        kernel_size,
        stride,
        padding,
        dilation,
        ceil_mode,
    )
    indices = prims._low_memory_max_pool_offsets_to_indices(
        offsets,
        kernel_size,
        x.shape[-dim:],
        stride,
        padding,
        dilation,
    )
    return vals, indices


def _max_pool_with_indices(
    x,
    kernel_size,
    stride,
    padding,
    dilation,
    ceil_mode,
    n_dim,
):
    kernel_size, stride, padding, dilation, _ = max_pool_checks(
        x, kernel_size, stride, padding, dilation, n_dim=n_dim
    )

    out, offsets = _max_pool_with_offsets(
        x, kernel_size, stride, padding, dilation, ceil_mode, n_dim=n_dim
    )

    indices = _low_memory_max_pool_offsets_to_indices(
        offsets,
        kernel_size,
        x.shape[-n_dim:],
        stride,
        padding,
        dilation,
    )

    return out, indices

