
def sample_inputs_mv(self, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, low=None, high=None, requires_grad=requires_grad)
    yield SampleInput(make_arg(S, M), make_arg(M))

