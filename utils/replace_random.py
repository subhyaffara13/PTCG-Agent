
def replace_random(
    match: Match,
    size,
    *,
    generator=None,
    dtype=None,
    device=None,
    layout=None,
    pin_memory=None,
):
    if generator is not None:
        return

    def replacement(size):
        result = inductor_prims.random(
            size, inductor_prims.seed(device), mode, **default_kwargs(device)
        )
        if dtype is not None:
            result = result.to(dtype)
        return result

    mode = {
        aten.rand: "rand",
        aten.randn: "randn",
    }[
        match.output_node().target.overloadpacket  # type: ignore[union-attr]
    ]  # type: ignore[union-attr]
    device = get_device(device)
    replacement_fn = replacement

    if mode == "rand" and config.align_random_eager and device.type == "cuda":
        # Only enable when align_random_eager is on.
        def replacement_align(size):
            offset = _shape_to_offset(size, device)

            align_dtype = dtype
            if isinstance(align_dtype, (tuple, list)):
                align_dtype = align_dtype[0] if len(align_dtype) else None

            result = inductor_prims.random(
                size,
                inductor_prims.rand_eager_offset(offset, device),
                mode,
                **default_kwargs(device),
                align_dtype=align_dtype,
            )
            if dtype is not None:
                result = result.to(dtype)
            return result

        replacement_fn = replacement_align

    # pyrefly: ignore [bad-argument-type]
    match.replace_by_example(replacement_fn, [size])

