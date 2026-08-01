
def sample_inputs_threshold(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    sizes = ((), (S,), (S, S), (S, S, S))
    for x_size in sizes:
        # threshold and values args must be numbers
        yield SampleInput(make_arg(x_size), make_arg(()).item(), make_arg(()).item())

