
def error_inputs_histogramdd(opinfo, device, **kwargs):
    invalid_bins = [1, 1, 1, 1, 1]
    make_arg = partial(make_tensor, dtype=torch.float, device=device, requires_grad=False)
    msg = "histogramdd: The size of bins must be equal to the innermost dimension of the input."
    yield ErrorInput(SampleInput(make_arg(5, 6), invalid_bins), error_regex=msg)

