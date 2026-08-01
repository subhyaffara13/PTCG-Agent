
def sample_inputs_std_var_unbiased(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype,
                       requires_grad=requires_grad)

    # Test var_mean(Tensor self, bool unbiased=True) -> (Tensor, Tensor)
    yield SampleInput(make_arg((S, S)), True)
    yield SampleInput(make_arg((S,)), False)

