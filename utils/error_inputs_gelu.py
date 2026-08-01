
def error_inputs_gelu(op, device, **kwargs):
    # Tests that gelu errors out when passed an approximation we don't know.
    yield ErrorInput(SampleInput(make_tensor((), dtype=torch.float, device=device), kwargs={"approximate": "asdf"}),
                     error_regex="approximate argument must be either")

