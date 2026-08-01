
def sample_inputs_comparison_ops(op, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_elementwise_binary(op, device, dtype, requires_grad, **kwargs)

    # Adds a sample input where both tensors have the same values
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    lhs = make_arg((S, S))
    yield SampleInput(lhs, args=(lhs.clone(),))

