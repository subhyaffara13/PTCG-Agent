
def sample_inputs_isin(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    # isin has two paths based on the size of elements and test_elements.
    # if elements.numel() < 10 * pow(test_elements.numel(), 0.145):
    yield SampleInput(make_arg((L,)), args=(make_arg((S,)),))
    # else:
    yield SampleInput(make_arg((S,)), args=(make_arg((L,)),))

