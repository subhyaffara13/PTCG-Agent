
def _rand_tensor_non_equal(*size):
    total = reduce(mul, size, 1)
    return torch.randperm(total).view(*size).double()

