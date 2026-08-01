
def sample_inputs_kron(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(
        make_tensor, dtype=dtype, device=device, requires_grad=requires_grad, low=None, high=None)
    test_cases = (
        ((S, S), (M, L)),
    )

    for input_shape, other_shape in test_cases:
        input = make_arg(input_shape)
        other = make_arg(other_shape)
        yield SampleInput(input, other)

