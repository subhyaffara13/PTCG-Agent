
def slice_scatter(
    input: Tensor,
    src: Tensor,
    dim: int = 0,
    start: int | None = None,
    end: int | None = None,
    step: int = 1,
):
    dim = utils.canonicalize_dim(input.ndim, dim)
    dim_size = input.shape[dim]
    start, end = _normalize_start_end(input, dim, start, end)

    src_size = list(input.shape)
    src_size[dim] = (end - start + (step - 1)) // step
    src = src.expand(src_size)

    if start == 0 and end == dim_size and step == 1:
        return src.clone()

    indices: list[Tensor | None] = [None] * input.dim()
    idx = torch.arange(dim_size, device=input.device)
    indices[dim] = (idx - start) // step

    mask = torch.ones(dim_size, device=input.device, dtype=torch.bool)
    if start != 0:
        mask = torch.logical_and(mask, idx >= start)

    if end != dim_size:
        mask = torch.logical_and(mask, idx < end)

    if step != 1:
        mask = torch.logical_and(mask, (idx - start) % step == 0)

    mask_shape = [1] * input.dim()
    mask_shape[dim] = -1
    mask = mask.view(mask_shape)
    return aten.where(mask, aten._unsafe_masked_index(src, mask, indices, 0), input)


def slice_scatter(x, src, dim=0, start=None, end=None, step=1):
    src = to_dtype(src, x.get_dtype())
    x_loader = x.make_loader()
    dim = _validate_dim(x, dim, 0)
    dim_size = x.get_size()[dim]

    # pyrefly: ignore [bad-argument-type]
    start, end = ir.SliceView.normalize_start_end(x, dim, start, end)

    src_size = list(x.get_size())
    src_size[dim] = FloorDiv(end - start + (step - 1), step)
    src = expand(src, src_size)
    src_loader = src.make_loader()

    def inner_fn(idx):
        if start == 0 and end == dim_size and step == 1:
            # selecting every element is the same as just src.clone()
            return src_loader(idx)

        idx_dim = ops.index_expr(idx[dim], torch.int64)
        src_idx = list(idx)
        src_idx[dim] = FloorDiv(idx[dim] - start, step)

        mask = []
        if start != 0:
            mask.append(
                ops.ge(
                    idx_dim,
                    ops.index_expr(sympy.expand(start), torch.int64),
                )
            )
        if end != dim_size:
            mask.append(
                ops.lt(
                    idx_dim,
                    ops.index_expr(sympy.expand(end), torch.int64),
                )
            )
        if step != 1:
            mask.append(
                ops.eq(
                    ops.index_expr(
                        ModularIndexing(idx[dim] - start, 1, step), torch.int64
                    ),
                    ops.constant(0, torch.int64),
                )
            )
        assert mask
        mask = functools.reduce(ops.and_, mask)
        src_val = ops.masked(
            mask,
            lambda: src_loader(src_idx),
            0 if is_integer_type(x) else 0.0,
        )
        return ops.where(
            mask,
            src_val,
            x_loader(idx),
        )

    return Pointwise.create(
        device=x.get_device(),
        dtype=x.get_dtype(),
        inner_fn=inner_fn,
        ranges=list(x.get_size()),
    )

