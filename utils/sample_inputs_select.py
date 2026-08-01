
def sample_inputs_select(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    yield SampleInput(make_arg(3, 5), args=(2,))


def sample_inputs_select(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    cases = (((S, S, S), (1, 2)),
             ((S, S, S), (-1, 2)),
             ((S, S, S), (-1, -1)),
             ((S, S, S), (1, -1)),
             ((S, S), (-1, 2)),
             ((S,), (0, 2))
             )

    for shape, args in cases:
        yield SampleInput(make_arg(shape), args=args)


def sample_inputs_select(op_info, device, dtype, requires_grad, **kwargs):
    for sample_input in sample_inputs_unary_dimwise(
        op_info, device, dtype, requires_grad, **kwargs
    ):
        # ragged dim chunking: test a single index
        if sample_input.kwargs["dim"] == sample_input.input._ragged_idx:
            yield _update_sample(sample_input, {"index": 0})
        # other dim chunking: test different indices
        else:
            D = sample_input.input.size(sample_input.kwargs["dim"])
            for index in [0, D // 2, D - 1]:
                yield _update_sample(sample_input, {"index": index})

