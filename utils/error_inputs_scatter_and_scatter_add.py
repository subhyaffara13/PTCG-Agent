
def error_inputs_scatter_and_scatter_add(op_info, device, **kwargs):
    # Error when self.dtype != src.dtype (and src is not a scalar)
    src = make_tensor((2, 5), device=device, dtype=torch.float32)
    idx = torch.tensor(((0, 1), (1, 2)), device=device, dtype=torch.long)
    dst = torch.zeros((3, 5), device=device, dtype=torch.float16 if torch.device(device).type == 'mps' else torch.double)
    yield ErrorInput(SampleInput(dst, args=(0, idx, src)),
                     error_regex="Expected self.dtype to be equal to src.dtype")

    # Index and destination must have the same number of dimensions
    src = make_tensor((2, 5), device=device, dtype=torch.float32)
    idx = torch.tensor(((0, 1), (1, 2)), device=device, dtype=torch.long)
    dst = torch.zeros((3, 5, 3), device=device, dtype=torch.float32)
    yield ErrorInput(SampleInput(dst, args=(0, idx, src)),
                     error_regex="Index tensor must have the same number of dimensions as self tensor")

    # Index and src must have the same number of dimensions when src is not a scalar
    src = make_tensor((2, 5, 2), device=device, dtype=torch.float32)
    idx = torch.tensor(((34, 1), (1, 2)), device=device, dtype=torch.long)
    dst = torch.zeros((3, 5), device=device, dtype=torch.float32)
    yield ErrorInput(SampleInput(dst, args=(0, idx, src)),
                     error_regex="Index tensor must have the same number of dimensions as src tensor")

    # Index out of bounds
    # NOTE: this ErrorInput is guarded because bounds checking does not occur on CUDA devices
    if torch.device(device).type == 'cpu':
        src = make_tensor((2, 5), device=device, dtype=torch.float32)
        idx = torch.tensor(((34, 1), (1, 2)), device=device, dtype=torch.long)
        dst = torch.zeros((3, 5), device=device, dtype=torch.float32)
        yield ErrorInput(SampleInput(dst, args=(0, idx, src)),
                         error_regex="index 34 is out of bounds for dimension 0 with size 3")

