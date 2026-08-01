
def sample_repeat_tile(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    rep_dims = ((), (0, ), (1, ), (0, 2), (1, 1), (2, 3), (2, 3, 2), (0, 2, 3), (2, 1, 1, 1),)
    shapes = ((), (0,), (2,), (3, 0), (3, 2), (3, 0, 1))

    if requires_grad:
        # Tests for variant_consistency_jit, grad, gradgrad
        # are slower. Use smaller bags of `rep_dims` and `shapes`
        # in this case.
        rep_dims = ((), (0, ), (0, 2), (1, 1), (2, 3), (1, 3, 2), (3, 1, 1))  # type: ignore[assignment]
        shapes = ((), (0,), (2,), (3, 2))  # type: ignore[assignment]

    is_repeat_op = op_info.name in ['repeat', '_refs.repeat']
    for rep_dim, shape in product(rep_dims, shapes):
        # `torch.repeat` errors for `len(rep_dims) < t.dim()`,
        # so we filter such combinations.
        if is_repeat_op and len(rep_dim) < len(shape):
            continue
        yield SampleInput(make_arg(shape), rep_dim)

