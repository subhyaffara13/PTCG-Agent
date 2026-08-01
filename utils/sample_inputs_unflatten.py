
def sample_inputs_unflatten(op_info, device, dtype, requires_grad, **kwargs):
    # in_shape, dim, sizes
    args = (((8,), 0, (8,)),
            ((8,), 0, (4, 2)),
            ((8,), -1, (2, 2, 2)),
            ((8,), -1, (-1, 2)),
            ((3, 6, 2), 1, (2, 3)),
            ((3, 6, 2), -2, (2, 3)),
            ((3, 6, 2), -2, (-1, 3)),
            ((3, 2, 12), 2, (3, 2, 2)),
            ((4, 0), 0, (2, 2)),
            ((4, 0), 1, (2, 0, 0, 0)),
            )
    make_tensor_partial = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    for in_shape, dim, sizes in args:
        yield SampleInput(make_tensor_partial(in_shape), args=(dim, sizes))


def sample_inputs_unflatten(op_info, device, dtype, requires_grad, **kwargs):
    for sample_input in sample_inputs_unary_dimwise(
        op_info, device, dtype, requires_grad, **kwargs
    ):
        # It will never make sense to operate on the ragged dim.
        # TODO: Handle this with error_inputs
        if sample_input.kwargs["dim"] == sample_input.input._ragged_idx:
            continue

        D = sample_input.input.size(sample_input.kwargs["dim"])
        # sizes should multiply to be D
        yield _update_sample(sample_input, {"sizes": [D, 1]})
        yield _update_sample(sample_input, {"sizes": [1, D]})
        if D % 2 == 0:
            yield _update_sample(sample_input, {"sizes": [D // 2, 2]})
            yield _update_sample(sample_input, {"sizes": [2, D // 2]})

