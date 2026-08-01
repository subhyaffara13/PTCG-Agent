
def sample_inputs_leaky_relu(op_info, device, dtype, requires_grad, **kwargs):
    N = 10
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    return (SampleInput(make_arg((N, N))) for _ in range(1, N))

