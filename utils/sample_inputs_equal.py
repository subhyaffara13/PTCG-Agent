
def sample_inputs_equal(op, device, dtype, requires_grad, **kwargs):
    make_arg = partial(
        make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    shapes = (
        ((), ()),
        ((S,), ()),
        ((), (S,)),
        ((S, 1), (S,)),
        ((M, S), ()),
        ((S, S), (S, S))
    )

    for shape_lhs, shape_rhs in shapes:
        lhs = make_arg(shape_lhs)
        rhs = make_arg(shape_rhs)
        broadcasts_input = shape_lhs != torch.broadcast_shapes(shape_lhs, shape_rhs)

        yield SampleInput(lhs, args=(rhs,), broadcasts_input=broadcasts_input)
        if shape_lhs == shape_rhs:
            yield SampleInput(lhs, args=(lhs.clone().detach_(),))

