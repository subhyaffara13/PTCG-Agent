
def rebuild_sparse_coo_tensor(
    rebuild_indices_func,
    rebuild_indices_args,
    rebuild_values_func,
    rebuild_values_args,
    shape,
    is_coalesced,
):
    indices = rebuild_indices_func(*rebuild_indices_args)
    values = rebuild_values_func(*rebuild_values_args)
    return torch.sparse_coo_tensor(indices, values, shape, is_coalesced=is_coalesced)

