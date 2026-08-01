
def sample_inputs_unravel_index(op_info, device, dtype, requires_grad, **kwargs):
    yield SampleInput(
        torch.tensor(
            [[3, 8, 13], [0, 5, 10]],
            device=device,
            dtype=dtype),
        (4, 5))
    yield SampleInput(
        torch.tensor([[3, 8, 13], [0, 5, 10]], device=device, dtype=dtype),
        (4, 2**30))
    yield SampleInput(
        torch.tensor([[3, 8, 13], [0, 5, 10]], device=device, dtype=dtype),
        (2**30, 4))
    yield SampleInput(
        torch.tensor(2, device=device, dtype=dtype),
        (2, 2))
    max_val = 2**(8 * dtype.itemsize - (1 if dtype.is_signed else 0)) - 1
    yield SampleInput(
        torch.tensor(max_val - 1, device=device, dtype=dtype),
        (1, max_val))
    yield SampleInput(
        torch.tensor([22, 41, 37], device=device, dtype=dtype),
        (7, 6))
    yield SampleInput(
        torch.tensor(min(1621, max_val), device=device, dtype=dtype),
        (6, 7, 8, 9))
    yield SampleInput(
        torch.tensor([], device=device, dtype=dtype),
        (10, 3, 5))
    yield SampleInput(
        torch.tensor(
            [[1, 0, 1, 2, 3, 4], [1, 6, 1, 3, 2, 0]],
            device=device,
            dtype=dtype),
        (5, 8))
    yield SampleInput(
        torch.tensor(
            [[1, 0, 1, 2, 3, 4], [1, 6, 1, 3, 2, 0], [1, 3, 1, 0, 9, 5]],
            device=device,
            dtype=dtype),
        (5, 8, 10))
    yield SampleInput(
        torch.tensor(0, device=device, dtype=dtype),
        ())

    a = np.array([[2, 4, 5, 6], [7, 8, 1, 15]])
    b = np.array([[3, 2, 7, 6], [10, 12, 8, 9]])
    _, i1, i2 = np.intersect1d(a, b, assume_unique=True, return_indices=True)
    yield SampleInput(torch.tensor(i1, device=device, dtype=dtype), a.shape)
    yield SampleInput(torch.tensor(i2, device=device, dtype=dtype), b.shape)

    a = np.array([[2, 4, 5, 6, 6], [4, 7, 8, 7, 2]])
    b = np.array([[3, 2, 7, 7], [10, 12, 8, 7]])
    _, i1, i2 = np.intersect1d(a, b, return_indices=True)
    yield SampleInput(torch.tensor(i1, device=device, dtype=dtype), a.shape)
    yield SampleInput(torch.tensor(i2, device=device, dtype=dtype), b.shape)

