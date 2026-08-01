
def error_inputs_masked_fill(op_info, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float, requires_grad=False)
    # `value` is not a 0-D tensor.
    yield ErrorInput(SampleInput(make_arg((2, 2)), args=(make_arg(()) > 0, make_arg((1,)))),
                     error_regex="only supports a 0-dimensional value tensor, but got tensor with 1 dimension")
    # downcasting complex value (scalar overload)
    yield ErrorInput(SampleInput(make_arg((2, 2)), args=(make_arg(()) > 0, 1j)),
                     error_regex=r"value cannot be converted to type .* without overflow")
    # downcasting complex value (tensor overload)
    yield ErrorInput(SampleInput(torch.ones(2, dtype=torch.long, device=device),
                                 args=(make_arg(()) > 0, torch.tensor(1j, device=device))),
                     error_regex=r"value cannot be converted to type .* without overflow")

    if torch.device(device).type == 'cuda':
        # `self` and `mask` on CPU but `value` is a CUDA scalar tensor.
        yield ErrorInput(SampleInput(torch.randn((S, S), device='cpu'),
                                     args=(torch.randn(S, S, device='cpu') > 0,
                                           torch.randn((), device='cuda'))),
                         error_regex=r"to be on same device")

