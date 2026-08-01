
def sample_inputs_repeat_interleave(op_info, device, dtype, requires_grad, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    yield SampleInput(make_input(()), repeats=2)
    yield SampleInput(make_input((2, 3, 4)), repeats=2)
    yield SampleInput(make_input((2, 3, 4)), repeats=2, dim=1)
    yield SampleInput(make_input((2, 3, 4)), repeats=torch.arange(3, device=device), dim=1)
    yield SampleInput(make_input((4, 1)), repeats=torch.arange(4, device=device), dim=0, output_size=6)

