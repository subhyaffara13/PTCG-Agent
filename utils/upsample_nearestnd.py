
def upsample_nearestnd(
    x,
    output_size,
    scales_x: tuple[float | None, ...],
    n: int = 2,
    exact: bool = False,
):
    x.realize_hint()  # elements are reused
    x_loader = x.make_loader()
    i_sizes = x.get_size()[-n:]
    batch = x.get_size()[:-n]
    i_sizes = [V.graph.sizevars.guard_int(i) for i in i_sizes]

    assert len(scales_x) == n
    o_sizes = output_size

    inv_scales = [i / o for i, o in zip(i_sizes, o_sizes)]
    for i, scale in enumerate(scales_x):
        if scale is not None:
            inv_scales[i] = 1.0 / scale

    def scale_fn(x, scale, size):
        # Nearest Exact: input_index = round(scale * (output_index + 0.5) - 0.5)
        #                            = floor(scale * (output_index + 0.5))
        # Nearest: input_index = floor(scale * output_index)
        x = ops.index_expr(x, torch.float32)
        if exact:
            x = ops.add(x, ops.constant(0.5, torch.float32))
        x = ops.mul(x, ops.constant(scale, torch.float32))
        x = ops.to_dtype(x, torch.int32)
        return ops.indirect_indexing(x, size, check=False)

    def fn(idx):
        x = idx[-n:]
        b = idx[:-n]
        return x_loader(
            [*b, *[scale_fn(i, s, size) for i, s, size in zip(x, inv_scales, i_sizes)]]
        )

    return Pointwise.create(
        device=x.get_device(),
        dtype=x.get_dtype(),
        inner_fn=fn,
        ranges=[*batch, *o_sizes],
    )

