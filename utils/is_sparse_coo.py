
def is_sparse_coo(t: object) -> TypeGuard[torch.Tensor]:
    return isinstance(t, torch.Tensor) and t.layout is torch.sparse_coo

