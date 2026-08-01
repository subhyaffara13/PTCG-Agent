
def sample_inputs_chunk(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    cases = (((S, S, S), (2,)),
             ((S, S, S), (S, 1)),
             ((S, S, S), (S, -1)))

    for case in cases:
        shape, args = case
        yield SampleInput(make_arg(shape), args=args)


def sample_inputs_chunk(op_info, device, dtype, requires_grad, **kwargs):
    for sample_input in sample_inputs_unary_dimwise(
        op_info, device, dtype, requires_grad, **kwargs
    ):
        # ragged dim chunking: test a single chunks value
        if sample_input.kwargs["dim"] == sample_input.input._ragged_idx:
            yield _update_sample(sample_input, {"chunks": 3})
        # other dim chunking: test different chunks values
        else:
            D = sample_input.input.size(sample_input.kwargs["dim"])
            for chunks in [1, D // 2, D - 1, D]:
                yield _update_sample(sample_input, {"chunks": chunks})

