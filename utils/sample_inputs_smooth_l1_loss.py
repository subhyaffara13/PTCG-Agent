
def sample_inputs_smooth_l1_loss(op_info, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_loss(op_info, device, dtype, requires_grad, **kwargs)

    make = partial(make_tensor, (S, S), device=device, dtype=dtype, requires_grad=requires_grad)

    # This test case always triggers the smooth condition, since absolute difference of input and target
    # is smaller than beta
    yield SampleInput(make(low=0, high=2), args=(make(low=-2, high=0),), kwargs=dict(beta=5))
    yield SampleInput(make(), args=(make(),), kwargs=dict(beta=0))

