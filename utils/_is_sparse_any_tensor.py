
def _is_sparse_any_tensor(obj: torch.Tensor):
    return _is_sparse_compressed_tensor(obj) or obj.layout is torch.sparse_coo

