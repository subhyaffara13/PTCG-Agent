
def error_inputs_softshrink(op, device, **kwargs):
    yield ErrorInput(SampleInput(make_tensor((1,), dtype=torch.float, device=device), kwargs={"lambd": -0.5}),
                     error_regex=r"lambda must be in range \[0,.*input dtype.*found -0\.5")

