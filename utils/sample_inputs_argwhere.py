
def sample_inputs_argwhere(op_info, device, dtype, requires_grad, **kwargs):
    yield SampleInput(torch.tensor([1, 0, 2, 0], dtype=dtype, device=device, requires_grad=requires_grad))
    mask = torch.tensor([[0, 1, 0, 1, 0],
                         [1, 1, 1, 1, 0],
                         [0, 0, 0, 1, 0],
                         [1, 0, 1, 1, 0],
                         [1, 0, 0, 1, 0]], dtype=torch.bool, device=device)
    t = make_tensor((S, S), dtype=dtype, device=device, requires_grad=requires_grad)
    t[mask] = 0
    yield SampleInput(t)

    t = make_tensor((S, S), dtype=dtype, device=device, requires_grad=requires_grad, noncontiguous=True)
    t[mask] = 0
    yield SampleInput(t)

    t = make_tensor((S, 0), dtype=dtype, device=device, requires_grad=requires_grad)
    yield SampleInput(t)

    yield SampleInput(torch.zeros((S,), dtype=dtype, device=device, requires_grad=requires_grad))
    yield SampleInput(make_tensor((), dtype=dtype, device=device, requires_grad=requires_grad))

