
def sample_inputs_lu(op_info, device, dtype, requires_grad=False, **kwargs):
    make_arg = partial(make_fullrank_matrices_with_distinct_singular_values,
                       dtype=dtype, device=device, requires_grad=requires_grad)

    # not needed once OpInfo tests support Iterables
    batch_shapes = ((), (3,), (3, 3))
    for batch_shape, get_infos, size_delta in product(batch_shapes, (True, False), (-2, -1, 0, +1, +2)):
        shape = batch_shape + (S + size_delta, S)
        input = make_arg(*shape)
        yield SampleInput(input, args=(True, get_infos))

