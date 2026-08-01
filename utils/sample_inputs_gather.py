
def sample_inputs_gather(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad, low=None, high=None)
    yield SampleInput(
        make_arg((M, S)),
        0,
        gather_variable((S, S), 1, M, True, device=device))
    yield SampleInput(
        make_arg((M, S)),
        0,
        gather_variable((S, S), 1, M, True, device=device).to(torch.int32))
    yield SampleInput(
        make_arg((M, S)),
        1,
        gather_variable((M, S // 2), 0, S, True, device=device))
    # Empty index tensor case, see: https://github.com/pytorch/pytorch/pull/65006
    yield SampleInput(
        make_arg((S,)),
        0,
        torch.tensor([], dtype=torch.uint8, device=device))
    yield SampleInput(
        make_arg((S,)),
        0,
        torch.tensor([[], []], dtype=torch.uint8, device=device))
    # 0D tensor case
    yield SampleInput(
        make_arg(()),
        0,
        torch.tensor([0], dtype=torch.int64, device=device))
    yield SampleInput(
        make_arg(()),
        0,
        torch.tensor(0, dtype=torch.int64, device=device))

