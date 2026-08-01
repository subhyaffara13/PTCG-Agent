
def is_sparse_compressed(t: object) -> TypeGuard[torch.Tensor]:
    return isinstance(t, torch.Tensor) and is_sparse_compressed_layout(t.layout)

