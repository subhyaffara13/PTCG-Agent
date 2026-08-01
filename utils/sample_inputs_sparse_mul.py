
def sample_inputs_sparse_mul(op_info, device, dtype, requires_grad, layout, **kwargs):
    """Sample inputs for mul operation on sparse tensors."""
    yield from _sample_inputs_sparse(
        sample_inputs_sparse_elementwise_binary_operation,
        _maybe_failing_sample_inputs_sparse_elementwise_binary_mul,
        _validate_sample_input_sparse_elementwise_binary_operation,
        op_info,
        device,
        dtype,
        requires_grad,
        layout,
        **kwargs,
    )

