
def sample_inputs_reduction_quantile(op_info, device, dtype, requires_grad, **kwargs):
    test_quantiles = (0.5, make_tensor((2,), dtype=dtype, device=device, low=0, high=1, requires_grad=requires_grad))
    test_interpolations = ['linear', 'midpoint']

    for quantiles in test_quantiles:
        for t in _generate_reduction_inputs(device, dtype, requires_grad):
            # Add case without dim and keepdim kwargs
            input = t.clone().requires_grad_(requires_grad)
            yield SampleInput(input, quantiles)
            for kwargs in _generate_reduction_kwargs(t.ndim, supports_multiple_dims=False):
                # Interpolation kwarg for now is only supported when providing both dim and keepdim
                kwargs.setdefault('dim', 0)
                kwargs.setdefault('keepdim', False)
                for interpolation in test_interpolations:
                    kwargs['interpolation'] = interpolation
                    input = t.clone().requires_grad_(requires_grad)
                    yield SampleInput(input, quantiles, **kwargs)

