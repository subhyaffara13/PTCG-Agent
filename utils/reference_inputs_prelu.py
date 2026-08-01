
def reference_inputs_prelu(op, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_prelu(op, device, dtype, requires_grad, **kwargs)
    yield from reference_inputs_elementwise_unary(op, device, dtype, requires_grad, **kwargs)

