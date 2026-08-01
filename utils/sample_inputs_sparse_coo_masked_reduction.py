
def sample_inputs_sparse_coo_masked_reduction(
    op_info, device, dtype, requires_grad, **kwargs
):
    """Sample inputs for masked reduction operators that support inputs
    with sparse coo layouts.
    """
    if op_info.supports_sparse:
        op_name = op_info.name.replace("masked.", "")
        for sample_input in sample_inputs_masked_reduction(
            op_info, device, dtype, requires_grad, **kwargs
        ):
            mask = sample_input.kwargs.get("mask")
            if mask is not None:
                sample_input_kwargs = sample_input.kwargs.copy()
                sample_input_kwargs.update(mask=mask.to_sparse())
                yield SampleInput(
                    sample_input.input.to_sparse(),
                    args=sample_input.args,
                    kwargs=sample_input_kwargs,
                )
            else:
                if op_name in {"prod", "amax", "amin"}:
                    # FIXME: for now reductions with non-zero reduction identity and
                    # unspecified mask are not supported for sparse COO
                    # tensors, see torch.masked.prod implementation
                    # for details.
                    continue
                yield SampleInput(
                    sample_input.input.to_sparse(),
                    args=sample_input.args,
                    kwargs=sample_input.kwargs,
                )

