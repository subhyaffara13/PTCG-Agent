
def error_inputs_flipud(op, device, **kwargs):
    yield ErrorInput(SampleInput(make_tensor((), dtype=torch.float, device=device)),
                     error_regex="Input must be >= 1-d.")

