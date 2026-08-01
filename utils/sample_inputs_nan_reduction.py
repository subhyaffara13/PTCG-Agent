
def sample_inputs_nan_reduction(supports_multiple_dims):
    # Generates sample inputs for reduction ops that contain the input tensor
    # and dim and keepdim kwargs. If a reduction op needs to test additional
    # args/kwargs then create a separate sample_inputs function
    def fn(op_info, device, dtype, requires_grad, **kwargs):
        for t in _generate_nan_reduction_inputs(device, dtype, requires_grad):
            # Add case without dim and keepdim kwargs
            yield SampleInput(t.clone().requires_grad_(requires_grad))
            for kwargs in _generate_reduction_kwargs(t.ndim, supports_multiple_dims):
                yield SampleInput(t.clone().requires_grad_(requires_grad), **kwargs)

    return fn

