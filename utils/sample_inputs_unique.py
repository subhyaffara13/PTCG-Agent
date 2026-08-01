
def sample_inputs_unique(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    sizes = ((), (S,), (S, S), (S, S, S), (S, 1, S), (S, 0, S))

    for shape, sorted, return_inverse, return_counts, dim in \
            product(sizes, [False, True], [False, True], [False, True], [None, -2, -1, 0, 1, 2]):
        # torch.unique cannot be called if the input tensor has a zero dimension which isn't the selected dim
        if 0 in shape and shape.index(0) is not dim:
            continue

        # skip invalid dim args
        if dim is not None and (dim < -len(shape) or dim >= len(shape)):
            continue

        kwargs = dict(sorted=sorted, return_inverse=return_inverse, return_counts=return_counts, dim=dim)

        # construct a test case with only one distinct value
        input_t = torch.zeros(shape, dtype=dtype, device=device, requires_grad=requires_grad)
        yield SampleInput(input_t, **kwargs)

        # construct a test case with mixed 0s and 1s
        input_t = make_arg(shape, dtype=torch.bool, requires_grad=False)\
            .to(dtype).requires_grad_(requires_grad)
        yield SampleInput(input_t, **kwargs)

        # construct a test case with many different values
        yield SampleInput(make_arg(shape), **kwargs)

