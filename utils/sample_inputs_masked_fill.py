
def sample_inputs_masked_fill(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    yield SampleInput(make_arg((S, S)), args=(torch.randn(S, S, device=device) > 0, 10))
    yield SampleInput(make_arg((S, S)), args=(torch.randn(S, S, device=device) > 0, make_arg(())))
    yield SampleInput(make_arg((S, S)), args=(torch.randn(S, device=device) > 0, 10))
    yield SampleInput(make_arg(()), args=(torch.randn((), device=device) > 0, 10))
    yield SampleInput(make_arg(()), args=(torch.randn((), device=device) > 0, make_arg(())))
    yield SampleInput(make_arg((S, S)), args=(torch.randn((), device=device) > 0, 10))

    yield SampleInput(make_arg((S,)),
                      args=(torch.randn(S, S, device=device) > 0, make_arg(())),
                      broadcasts_input=True)
    yield SampleInput(make_arg((S,)),
                      args=(torch.randn(S, S, device=device) > 0, 10),
                      broadcasts_input=True)

    if torch.device(device).type == 'cuda':
        # `self` and `mask` on CUDA but `value` is a CPU scalar tensor.
        yield SampleInput(make_arg((S, S)),
                          args=(torch.randn(S, S, device=device) > 0,
                                make_tensor((), device="cpu", dtype=dtype)))

