
def sample_inputs_rrelu(op_info, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_elementwise_unary(
        op_info, device, dtype, requires_grad, op_kwargs=dict(lower=0., upper=1., training=True))

    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    yield SampleInput(make_arg(S))
    yield SampleInput(make_arg(S), training=False)

