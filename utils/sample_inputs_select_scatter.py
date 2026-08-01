
def sample_inputs_select_scatter(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    cases = (((S, S, S), (S, S), (1, 2)),
             ((S, S, S), (S, S), (-1, 2)),
             ((S, S, S), (S, S), (-1, -1)),
             ((S, S, S), (S, S), (1, -1)),
             ((S,), (), (0, 2))
             )

    for input_shape, src_shape, args in cases:
        input_ = make_arg(input_shape)
        src = make_arg(src_shape)
        yield SampleInput(input_, args=(src, *args))

