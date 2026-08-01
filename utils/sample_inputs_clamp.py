
def sample_inputs_clamp(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, low=None, high=None, requires_grad=requires_grad)
    make_integral_arg = partial(make_tensor, dtype=torch.int32, device=device, low=None, high=None, requires_grad=False)
    shape = (S, M, S)

    yield SampleInput(make_arg(shape), args=(make_arg(shape), make_arg(shape)))
    yield SampleInput(make_arg(shape), args=(make_arg(shape[1:]), make_arg(shape[1:])))
    yield SampleInput(make_arg(shape), args=(make_arg((S, 1, S)),))
    yield SampleInput(make_arg(shape), args=(None, make_arg(shape)))
    yield SampleInput(make_arg(shape), args=(make_arg(shape), None))
    # test type promotion
    yield SampleInput(make_arg(shape), args=(make_integral_arg(shape), None))
    yield SampleInput(make_arg(shape), args=(make_arg(shape), make_integral_arg(shape)))

