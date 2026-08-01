
def error_inputs_fliplr(op, device, **kwargs):
    yield ErrorInput(SampleInput(make_tensor((1,), dtype=torch.float, device=device)),
                     error_regex="Input must be >= 2-d.")

