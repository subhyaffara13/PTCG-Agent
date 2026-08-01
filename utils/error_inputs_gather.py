
def error_inputs_gather(op_info, device, **kwargs):
    # src is [1, 2]
    #        [3, 4]
    src = torch.tensor(((1, 2), (3, 4)), device=device, dtype=torch.float32)

    # idx is [0, 0]
    #        [1, 0]
    idx = torch.tensor(((0, 0), (1, 0)), device=device, dtype=torch.long)

    # Index should be smaller than self except on dimension 1
    bad_src = make_tensor((1, 1), device=device, dtype=torch.float32)
    yield ErrorInput(SampleInput(bad_src, args=(1, idx,)),
                     error_regex="Size does not match at dimension 0")

    # TODO: FIXME
    # out.dtype must match src.dtype
    # Creates new src & idx since SampleInputs can't share tensors
    src = torch.tensor(((1, 2), (3, 4)), device=device, dtype=torch.float32)
    idx = torch.tensor(((0, 0), (1, 0)), device=device, dtype=torch.long)
    out = torch.empty((2, 2), device=device, dtype=torch.float16 if torch.device(device).type == 'mps' else torch.float64)
    yield ErrorInput(SampleInput(src, args=(1, idx), kwargs={'out': out}),
                     error_regex="Expected out tensor to have dtype")

    # src and index tensors must have the same # of dimensions
    # idx too few dimensions
    src = torch.tensor(((1, 2), (3, 4)), device=device, dtype=torch.float32)
    idx = torch.tensor((0, 0), device=device, dtype=torch.long)
    yield ErrorInput(SampleInput(src, args=(1, idx)),
                     error_regex="Index tensor must have the same number of dimensions")

    # src too few dimensions
    src = torch.tensor((1, 2), device=device, dtype=torch.float32)
    idx = torch.tensor(((0, 0), (1, 0)), device=device, dtype=torch.long)
    yield ErrorInput(SampleInput(src, args=(0, idx)),
                     error_regex="Index tensor must have the same number of dimensions")

    # index out of bounds
    # NOTE: this ErrorInput is guarded because bounds checking does not occur on CUDA devices
    if torch.device(device).type == 'cpu':
        src = torch.tensor(((1, 2), (3, 4)), device=device, dtype=torch.float32)
        idx = torch.tensor(((0, 23), (1, 0)), device=device, dtype=torch.long)
        yield ErrorInput(SampleInput(src, args=(1, idx,)),
                         error_regex="index 23 is out of bounds for dimension")

    x = torch.rand((1,), device=device).expand((3,))
    src = torch.rand((6,), device=device)
    ind = torch.tensor([2, 1, 0], device=device, dtype=torch.int64)

    yield ErrorInput(SampleInput(src, args=(0, ind,), kwargs=dict(out=x)),
                     error_type=RuntimeError,
                     error_regex='unsupported operation')

    yield ErrorInput(SampleInput(src, args=(0, ind,), kwargs=dict(out=src)),
                     error_type=RuntimeError,
                     error_regex='unsupported operation')

    yield ErrorInput(SampleInput(ind.clone(), args=(0, ind[1:],), kwargs=dict(out=ind[:1])),
                     error_type=RuntimeError,
                     error_regex='unsupported operation')

