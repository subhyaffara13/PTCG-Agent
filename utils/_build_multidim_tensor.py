
def _build_multidim_tensor(dim, dim_size, value=None, dtype=torch.float):
    if value is None:
        value = dim
    return torch.empty(size=[dim_size for _ in range(dim)], dtype=dtype).fill_(value)

