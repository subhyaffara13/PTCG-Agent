
def sample_inputs_cumulative_ops(op_info, device, dtype, requires_grad, supports_dtype_kwargs=True, **kwargs):
    def _make_tensor_helper(shape, low=None, high=None):
        return make_tensor(shape, dtype=dtype, device=device, low=low, high=high, requires_grad=requires_grad)

    yield SampleInput(_make_tensor_helper((S, S, S)), 0)
    yield SampleInput(_make_tensor_helper((S, S, S)), 1)
    yield SampleInput(_make_tensor_helper(()), 0)

    if supports_dtype_kwargs:
        # NOTE: if `dtype` is not same as input, then inplace variants fail with
        # `provided dtype must match the dtype of self tensor in cumsum`
        yield SampleInput(_make_tensor_helper((S, S, S)), 1, dtype=dtype)

