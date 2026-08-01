
def sample_inputs_masked_scatter(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    yield SampleInput(make_arg((S, S)), args=(torch.randn(S, S, device=device) > 0, make_arg((S, S))))
    yield SampleInput(make_arg((S, S)), args=(torch.randn((S,), device=device) > 0, make_arg((S, S))))
    yield SampleInput(make_arg((S, S)), args=(bernoulli_scalar().to(device), make_arg((S, S))))
    yield SampleInput(make_arg((S,)),
                      args=(torch.randn(S, S, device=device) > 0, make_arg((S, S))),
                      broadcasts_input=True)

