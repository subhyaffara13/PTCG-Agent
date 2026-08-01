
def sample_inputs_masked_normalize(op_info, device, dtype, requires_grad, **kwargs):
    """Sample inputs for masked normalize."""
    for ord in [2.0, 1, float("inf"), float("-inf"), 0]:
        for sample_input in sample_inputs_softmax_variant(
            op_info, device, dtype, requires_grad, use_zero_dimensions=False, **kwargs
        ):
            yield SampleInput(
                sample_input.input.clone().requires_grad_(requires_grad),
                ord,
                *sample_input.args,
                **sample_input.kwargs,
            )

