
def select_scatter(x, src, dim: int, index: int):
    src = to_dtype(src, x.get_dtype())
    x_loader = x.make_loader()
    dim = _validate_dim(x, dim, 0)
    if V.graph.sizevars.guard_or_false(sympy.Lt(index, 0)):
        index = index + x.get_size()[dim]
    elif V.graph.sizevars.guard_or_false(sympy.Ge(index, 0)):
        pass
    else:
        # unbacked index
        return fallback_handler(aten.select_scatter.default)(x, src, dim, index)

    V.graph.sizevars.check_leq(0, index)  # type: ignore[arg-type]
    V.graph.sizevars.check_lt(index, x.get_size()[dim])  # type: ignore[arg-type]
    src = expand(unsqueeze(src, dim), x.get_size())
    src_loader = src.make_loader()

    def inner_fn(idx):
        return ops.where(
            ops.eq(
                ops.index_expr(idx[dim], torch.int32),
                ops.index_expr(index, torch.int32),
            ),
            src_loader(idx),
            x_loader(idx),
        )

    return Pointwise.create(
        device=x.get_device(),
        dtype=x.get_dtype(),
        inner_fn=inner_fn,
        ranges=list(x.get_size()),
    )


def select_scatter(x: TensorLikeType, src: TensorLikeType, dim: int, index: int):
    dim = utils.canonicalize_dim(x.ndim, dim)
    mask_shape = [1] * x.ndim
    mask_shape[dim] = -1
    if index < 0:
        index = index + x.shape[dim]
    mask = torch.arange(x.shape[dim], device=x.device).view(mask_shape) == index
    src = torch.unsqueeze(src, dim).expand(x.shape)
    return torch.where(mask, src, x)

