
def sample_inputs_masked_cumops(op_info, device, dtype, requires_grad, **kwargs):
    """Sample inputs for masked cumsum and cumprod."""
    for sample_input in sample_inputs_softmax_variant(
        op_info, device, dtype, requires_grad, **kwargs
    ):
        for mask in _generate_masked_op_mask(
            sample_input.input.shape, device, **kwargs
        ):
            if type(mask) is not torch.Tensor:
                continue
            sample_input_args, sample_input_kwargs = (
                sample_input.args,
                dict(mask=mask, **sample_input.kwargs),
            )
            if "keepdim" in sample_input_kwargs:
                sample_input_kwargs.pop("keepdim")
            # dimension is required
            if sample_input_args:
                dim = sample_input.args[0]
            else:
                if "dim" not in sample_input_kwargs:
                    continue
                dim = sample_input_kwargs.pop("dim")
                sample_input_args = (dim,)
            yield SampleInput(
                sample_input.input.clone().requires_grad_(requires_grad),
                *sample_input_args,
                **sample_input_kwargs,
            )

