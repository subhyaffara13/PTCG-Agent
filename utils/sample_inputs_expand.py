
def sample_inputs_expand(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    cases = (((S, 1, 1), (S, S, S)),
             ((S, 1, S), (S, S, S)),
             ((S, 1, S), (-1, S, -1)),
             ((S, 1, S), (-1, S, S)),
             ((S, 1), (S, S, S)),
             ((1,), (S, S, S)),
             ((1, S), (1, 1, S)),
             ((), ()),
             ((), (1, 3, 2)),
             )

    for case in cases:
        shape, args = case
        yield SampleInput(make_arg(shape), args=(args,))

