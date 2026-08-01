
def sample_inputs_bucketize(op_info, device, dtype, requires_grad, reference_inputs_mode=False, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    sizes = (((), S), ((S,), S), ((S, S), S), ((S, S, S), S), ((S, 1, S), S), ((S, 0, S), S))

    if reference_inputs_mode:
        sizes += (((256,), 128), ((128,), 256), ((32, 32), 11), ((32, 4, 32), 33))

    for (input_shape, nb), out_int32, right in product(sizes, [False, True], [False, True]):
        input_tensor = make_arg(input_shape)
        boundaries = make_arg(nb).msort()

        yield SampleInput(input_tensor, boundaries,
                          out_int32=out_int32, right=right)

