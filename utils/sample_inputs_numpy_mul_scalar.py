
def sample_inputs_numpy_mul_scalar(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    yield SampleInput(make_arg(4, low=0.9, high=2), args=(), kwargs={"scalar": 3.14})

