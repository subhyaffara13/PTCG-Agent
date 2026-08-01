
def _create_range_input_gen_fn(
    base_gen_fn: Callable[[torch.Tensor], torch.Tensor],
    dim_index: int,
    range_start: int,
    range_end: int | float,
    range_upper_bound: int,
) -> Callable[[torch.Tensor], torch.Tensor]:
    """Create input generator that modifies target dimension to top of range.
    range_upper_bound: Size to use for benchmarking when range_end is unbounded.
    Default is DEFAULT_RANGE_UPPER_BOUND = 65536
    """
    from torch._inductor.ir import get_fill_order
    from torch._inductor.kernel.flex.common import construct_strides

    target_dim = range_upper_bound if range_end == float("inf") else int(range_end)

    def constrained_gen_fn(fake_tensor: torch.Tensor) -> torch.Tensor:
        result = base_gen_fn(fake_tensor)
        shape = list(result.shape)
        shape[dim_index] = target_dim

        # We modified the shape of the result, so we need to recalculate the strides
        # TODO: Refine this to a better way to more directly preserve strides
        fill_order = get_fill_order(result.stride(), shape_env=None)
        new_stride = construct_strides(shape, fill_order)

        storage_size = sum((s - 1) * st for s, st in zip(shape, new_stride)) + 1
        storage = torch.randn(storage_size, dtype=result.dtype, device=result.device)
        return storage.as_strided(shape, tuple(new_stride))

    return constrained_gen_fn

