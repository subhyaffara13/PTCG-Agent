
def error_inputs_bucketize(opinfo, device, **kwargs):
    make_arg = partial(make_tensor, dtype=torch.float, device=device, requires_grad=False)
    yield ErrorInput(SampleInput(make_arg((S, S, S)), make_arg((S, S))),
                     error_regex="boundaries tensor must be 1 dimension")

