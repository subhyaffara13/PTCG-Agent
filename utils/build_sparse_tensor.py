
def build_sparse_tensor(coalesce=False, requires_grad=True, dtype=torch.float32):
    i = [[0, 1, 1], [2, 0, 2]]
    v = [3.2, 4.1, 5.3]
    tensor = torch.sparse_coo_tensor(
        i, v, (3, 3), requires_grad=requires_grad, dtype=dtype
    )
    if coalesce:
        tensor = tensor.coalesce()
    return tensor


def build_sparse_tensor(coalesce=False):
    i = [[0, 1, 1], [2, 0, 2]]
    v = [3, 4, 5]
    tensor = torch.sparse_coo_tensor(i, v, (2, 3))
    if coalesce:
        tensor = tensor.coalesce()
    return tensor

