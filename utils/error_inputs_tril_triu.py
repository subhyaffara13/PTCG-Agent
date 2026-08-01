
def error_inputs_tril_triu(opinfo, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float32)

    # error inputs for input.ndim <= 2
    yield ErrorInput(SampleInput(make_arg((4,))), error_regex="input tensor must have at least 2 dimensions")

