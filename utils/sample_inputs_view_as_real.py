
def sample_inputs_view_as_real(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    sizes = ((S, S), ())
    return (SampleInput(make_arg(size)) for size in sizes)

