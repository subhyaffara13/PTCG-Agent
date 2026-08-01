
def sample_inputs_dot_vdot(self, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    def make_arg_conj(size):
        return make_arg(size).conj().requires_grad_(requires_grad)

    yield SampleInput(make_arg((S, )), make_arg((S, )))
    if dtype.is_complex:
        # dot/vdot for (conj(input), conj(arg_tensor)) and (conj(input), arg_tensor)
        # is tested in test_conj_view (which tests operations with only conjugated input tensor
        # -- not conjugated arg tensors)
        yield SampleInput(make_arg((S, )), make_arg_conj((S, )))

