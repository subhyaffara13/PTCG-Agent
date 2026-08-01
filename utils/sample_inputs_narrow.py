
def sample_inputs_narrow(op_info, device, dtype, requires_grad, **kwargs):
    for sample_input in sample_inputs_unary_dimwise(
        op_info, device, dtype, requires_grad, **kwargs
    ):
        # ragged dim narrowing: test a single start, length value
        if sample_input.kwargs["dim"] == sample_input.input._ragged_idx:
            yield _update_sample(sample_input, {"start": 1, "length": 2})
        # other dim narrowing: test different start, length values
        else:
            D = sample_input.input.size(sample_input.kwargs["dim"])
            for start, length in [(0, D), (0, D - 1), (1, D - 1), (D - 1, 1)]:
                yield _update_sample(sample_input, {"start": start, "length": length})

