
def sample_inputs_elementwise_njt_unary(
    op_info, device, dtype, requires_grad, op_kwargs=None, **kwargs
):
    if not op_kwargs:
        op_kwargs = {}

    for njt in _sample_njts(
        device=device, dtype=dtype, requires_grad=requires_grad, dims=[2, 3, 4]
    ):
        yield SampleInput(njt, kwargs=dict(op_kwargs), name=_describe_njt(njt))

