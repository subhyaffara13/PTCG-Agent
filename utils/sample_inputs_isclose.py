
def sample_inputs_isclose(op, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_elementwise_binary(op, device, dtype, requires_grad, **kwargs)

    # Creates additional inputs to test the rtol, atol, and equal_nan params
    rtols = [0., 1e-7]
    atols = [0., 1e-7]
    equal_nans = [False, True]

    products = product(rtols, atols, equal_nans)

    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    for rtol, atol, equal_nan in products:
        lhs = make_arg((S, S), **op.lhs_make_tensor_kwargs)
        rhs = make_arg((S, S), **op.rhs_make_tensor_kwargs)

        yield SampleInput(lhs, args=(rhs,),
                          kwargs=dict(rtol=rtol, atol=atol, equal_nan=equal_nan))

