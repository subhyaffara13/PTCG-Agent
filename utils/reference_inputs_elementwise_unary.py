
def reference_inputs_elementwise_unary(op, device, dtype, requires_grad, **kwargs):
    gen = partial(
        _reference_inputs_elementwise_unary, op, device, dtype, requires_grad, **kwargs
    )

    # yields "normal" samples
    yield from gen()

    # yields noncontiguous samples
    for sample in gen():
        yield sample.noncontiguous()

    yield from generate_elementwise_unary_noncontiguous_tensors(
        op, device=device, dtype=dtype, requires_grad=requires_grad, **kwargs
    )

    yield from generate_elementwise_unary_arbitrarily_strided_tensors(
        op, device=device, dtype=dtype, requires_grad=requires_grad, **kwargs
    )

