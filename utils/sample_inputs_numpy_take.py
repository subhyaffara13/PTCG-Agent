
def sample_inputs_numpy_take(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    tensor = make_arg(3, 5)
    dim = 1
    _, ind, ind_inv = NumpySort.apply(tensor, 1)
    yield SampleInput(tensor, args=(ind, ind_inv, dim))

