
def is_sparse_any(t: object) -> TypeGuard[torch.Tensor]:
    return is_sparse_coo(t) or is_sparse_compressed(t)

