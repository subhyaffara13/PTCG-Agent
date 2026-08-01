
def sample_inputs_sort(op_info, device, dtype, requires_grad, **kwargs):
    def small_3d_unique():
        res = torch.randperm(S * S * S, dtype=torch.int64, device=device).view(S, S, S)
        res = res.to(dtype).requires_grad_(requires_grad)
        return res

    def large_1d_unique():
        res = torch.randperm(L * L * L, dtype=torch.int64, device=device)
        res = res.to(dtype).requires_grad_(requires_grad)
        return res

    # Test case for large tensor.
    yield SampleInput(large_1d_unique())

    # Test cases for small 3d tensors.
    # Imitates legacy tests from test/test_torch.py
    dims = range(-3, 3)
    flag = [True, False]
    for dim, descending, stable in product(dims, flag, flag):
        # default schema without stable sort
        if not (dtype == torch.bool and torch.device(device).type == 'cuda'):
            # bool and cuda requires stable sort for stable results, at least
            # for the return index
            yield SampleInput(small_3d_unique(), dim, descending)
        # schema with stable sort, no CUDA support yet
        if torch.device(device).type == 'cpu':
            yield SampleInput(
                small_3d_unique(), dim=dim, descending=descending, stable=stable)

    # Test cases for scalar tensor
    tensor_opt = dict(dtype=dtype, device=device, requires_grad=requires_grad)
    yield SampleInput(torch.tensor(1, **tensor_opt))
    yield SampleInput(torch.tensor(1, **tensor_opt), 0)
    yield SampleInput(torch.tensor(1, **tensor_opt), 0, True)

    # Test cases for empty tensor
    yield SampleInput(torch.tensor((), **tensor_opt))
    yield SampleInput(torch.tensor((), **tensor_opt), 0)
    yield SampleInput(torch.tensor((), **tensor_opt), 0, True)

    # Test cases for stable sort
    yield SampleInput(small_3d_unique(), stable=True)
    yield SampleInput(small_3d_unique(), dim=0, stable=True)
    yield SampleInput(small_3d_unique(), dim=0, descending=True, stable=True)

