
def reference_inputs_logsumexp(op, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_logsumexp(op, device, dtype, requires_grad, **kwargs)

    # https://github.com/pytorch/pytorch/issues/91843
    t = torch.tensor([20, 30, 100], dtype=dtype, device=device, requires_grad=requires_grad)
    yield SampleInput(t, 0, False)

    t = torch.tensor((), dtype=dtype, device=device, requires_grad=requires_grad)
    yield SampleInput(t, 0, False)

    # tests masking
    # https://github.com/pytorch/pytorch/pull/91860#pullrequestreview-1241344073
    t = torch.tensor(float("inf"))
    yield SampleInput(t, 0, True)

