
def error_inputs_cov(op_info, device, **kwargs):
    a = torch.rand(S, device=device)
    yield ErrorInput(
        SampleInput(torch.rand(S, S, S, device=device)),
        error_regex="expected input to have two or fewer dimensions")
    yield ErrorInput(
        SampleInput(a, fweights=torch.rand(S, S, device=device)),
        error_regex="expected fweights to have one or fewer dimensions")
    yield ErrorInput(
        SampleInput(a, aweights=torch.rand(S, S, device=device)),
        error_regex="expected aweights to have one or fewer dimensions")
    yield ErrorInput(
        SampleInput(a, fweights=torch.rand(S, device=device)),
        error_regex="expected fweights to have integral dtype")
    yield ErrorInput(
        SampleInput(a, aweights=torch.tensor([1, 1], device=device)),
        error_regex="expected aweights to have floating point dtype")
    yield ErrorInput(
        SampleInput(a, fweights=torch.tensor([1], device=device)),
        error_regex="expected fweights to have the same numel")
    yield ErrorInput(
        SampleInput(a, aweights=torch.rand(1, device=device)),
        error_regex="expected aweights to have the same numel")
    yield ErrorInput(
        SampleInput(a, fweights=torch.tensor([-1, -2, -3, -4 , -5], device=device)),
        error_regex="fweights cannot be negative")
    yield ErrorInput(
        SampleInput(a, aweights=torch.tensor([-1., -2., -3., -4., -5.], device=device)),
        error_regex="aweights cannot be negative")

