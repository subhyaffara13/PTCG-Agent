
def sample_inputs_jiterator(op, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    shapes = (
        ((), ()),
        ((S,), ()),
        ((S, 1), (S,)),
        ((M, S), ()),
        ((S, M, S), (M, S)),
        ((S, M, S), (S, M, S)),
        ((M, 1, S), (M, S)),
        ((M, 1, S), (1, M, S)),
        ((0, 1, 3), (0, 10, 3))
    )

    num_inputs = kwargs.get('num_inputs')
    sample_kwargs = kwargs.get('sample_kwargs', {})

    for shape_lhs, shape_rhs in shapes:
        lhs = make_arg(shape_lhs)
        args = [make_arg(shape_rhs) for _ in range(num_inputs - 1)]
        broadcasts_input = (shape_lhs != torch.broadcast_shapes(shape_lhs, shape_rhs))

        yield SampleInput(lhs, args=tuple(args), kwargs=sample_kwargs, broadcasts_input=broadcasts_input)

