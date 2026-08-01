
def error_inputs_sparse_like_fns(op_info, device, layout, **kwargs):
    """Error inputs for like-functions on sparse tensors."""
    dtype = torch.float64
    requires_grad = False
    yield from _error_inputs_sparse(
        _maybe_failing_sample_inputs_sparse_like_fns,
        _validate_sample_input_sparse_like_fns,
        op_info,
        device,
        dtype,
        requires_grad,
        layout,
        **kwargs,
    )

