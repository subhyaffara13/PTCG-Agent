
def inductor_random(
    size: list[int],
    seed: TensorBox,
    mode: str,
    *,
    offset: int = 0,
    align_dtype: torch.dtype = torch.float32,
):
    assert not config.fallback_random
    assert mode in ("rand", "randn")
    size = [*size]
    dtype = torch.float32
    device = seed.get_device_or_error()
    random_pos = ir.FixedLayout(
        device, dtype, size, ir.FlexibleLayout.contiguous_strides(size), offset=offset
    ).make_indexer()
    seed_loader = seed.make_loader()

    if config.align_random_eager and device.type == "cuda":
        threads_per_round = get_threads_per_round(device)

        def _vec_from_dtype(dt: torch.dtype) -> int:
            if dt in (torch.float16, torch.bfloat16):
                return 8
            return 4

        vec = _vec_from_dtype(align_dtype)

        def inner_fn(index):
            rng_seed = seed_loader([0])
            base_offset = seed_loader([1])
            return ops.rand_eager(
                rng_seed,
                base_offset,
                threads_per_round,
                ops.index_expr(random_pos(index), torch.int32),
                vec=int(vec),
            )
    else:

        def inner_fn(index):
            return getattr(ops, mode)(
                seed_loader([]),
                ops.index_expr(random_pos(index), torch.int32),
            )

    result = Pointwise.create(
        device=device,
        dtype=dtype,
        inner_fn=inner_fn,
        ranges=[*size],
    )
    result.realize()
    return result

