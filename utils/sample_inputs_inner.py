
def sample_inputs_inner(self, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    yield SampleInput(make_arg(S), make_arg(S))
    yield SampleInput(make_arg(), make_arg(S, S))

