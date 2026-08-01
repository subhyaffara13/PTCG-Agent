
def _to_flat_dense_if_sparse(tensor):
    if _is_sparse_any_tensor(tensor):
        return tensor.to_dense().reshape(-1)
    else:
        return tensor

