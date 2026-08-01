
def reduce_scatter_tensor_autograd(
    self: torch.Tensor,
    reduceOp: str,
    scatter_dim: int,
    group: RANK_TYPES,
    tag: str = "",
):
    """
    Reduces the tensor data across all machines in such a way that all get
    the final result, then scatter the results to corresponding ranks.

    This function is the same as reduce_scatter_tensor but will propagate the
    backwards gradient across workers.

    Currently only the "sum" reduceOp is supported.

    See reduce_scatter_tensor for more details on usage.
    """

    group = _resolve_group(group, tag)
    group_size = c10d._get_group_size_by_name(group)

    if self.size(scatter_dim) % group_size != 0:
        raise AssertionError(
            f"input dimension 0 ({self.size(0)} must be a multiple of group_size {group_size}"
        )
    if scatter_dim != 0:
        self = _chunk_or_narrow_cat(self, group_size, narrow_dim=scatter_dim, cat_dim=0)

    tensor = torch.ops._c10d_functional_autograd.reduce_scatter_tensor(
        self,
        reduceOp.lower(),
        group_size,
        _group_or_group_name(group),
    )
    res = _FromTorchTensor.apply(tensor)
    return res

