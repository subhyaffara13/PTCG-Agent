
def sample_inputs_slice_scatter(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    cases = (((L, L, L), (L, L, L,), (0, 0, L, 1)),
             ((L, L, L), (L // 2, L, L,), (0, L // 2, L, 1)),
             ((L, L, L), (L // 4, L, L,), (0, L // 2, L, 2)),
             ((L, L, L), (L, L, L,), (1, 0, L, 1)),
             ((L, L, L), (L, L // 2, L,), (1, L // 2, L, 1)),
             ((L, L, L), (L, L // 4, L,), (1, L // 2, L, 2)),
             ((L, L, L), (L, L, L,), (2, 0, L, 1)),
             ((L, L, L), (L, L, L // 2,), (2, L // 2, L, 1)),
             ((L, L, L), (L, L, L // 4,), (2, L // 2, L, 2)),
             )

    for input_shape, src_shape, args in cases:
        input_ = make_arg(input_shape)
        src = make_arg(src_shape)
        yield SampleInput(input_, args=(src, *args))

