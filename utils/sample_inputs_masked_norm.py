
def sample_inputs_masked_norm(op_info, device, dtype, requires_grad, **kwargs):
    """Sample inputs for masked norm."""
    for ord in [2.0, 1, float("inf"), float("-inf"), 0]:
        for sample_input in sample_inputs_masked_reduction(
            op_info, device, dtype, requires_grad, **kwargs
        ):
            sample_input_args, sample_input_kwargs = (
                (ord,) + sample_input.args,
                sample_input.kwargs.copy(),
            )
            yield SampleInput(
                sample_input.input.clone().requires_grad_(requires_grad),
                args=sample_input_args,
                kwargs=sample_input_kwargs,
            )

