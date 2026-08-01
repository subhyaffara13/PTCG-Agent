
def sample_inputs_expand_as(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device)

    cases = (((S, 1, 1), (S, S, S)),
             ((), ()),
             ((), (1, 1)),
             )

    for shape, shape_other in cases:
        yield SampleInput(make_arg(shape, requires_grad=requires_grad),
                          args=(make_arg(shape_other, requires_grad=False),))

