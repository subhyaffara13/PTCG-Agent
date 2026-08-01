
def sample_inputs_mm(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    def make_arg_conj(size):
        return make_arg(size).conj().requires_grad_(requires_grad)

    first_shape, second_shape = (S, M), (M, S)

    yield SampleInput(make_arg(first_shape), args=(make_arg(second_shape),))

    if dtype.is_complex:
        yield SampleInput(make_arg(first_shape), args=(make_arg_conj(second_shape),))

    # Matmul of empty matrices
    yield SampleInput(make_arg((0, S)), args=(make_arg(S, M),))
    yield SampleInput(make_arg((S, 0)), args=(make_arg(0, M),))

