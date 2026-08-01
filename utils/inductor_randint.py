
def inductor_randint(
    low: int, high: int, size: list[int], seed: TensorBox, *, offset: int = 0
):
    assert not config.fallback_random
    size = [*size]
    dtype = torch.int64
    device = seed.get_device_or_error()
    random_pos = ir.FixedLayout(
        device, dtype, size, ir.FlexibleLayout.contiguous_strides(size), offset=offset
    ).make_indexer()
    seed_loader = seed.make_loader()

    def inner_fn(index):
        return ops.randint64(
            seed_loader([]),
            ops.index_expr(random_pos(index), torch.int32),
            ops.index_expr(low, torch.int64),
            ops.index_expr(high, torch.int64),
        )

    return Pointwise.create(
        device=device,
        dtype=dtype,
        inner_fn=inner_fn,
        ranges=[*size],
    )

