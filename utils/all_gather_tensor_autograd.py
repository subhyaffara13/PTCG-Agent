
def all_gather_tensor_autograd(
    self: torch.Tensor,
    gather_dim: int,
    group: RANK_TYPES,
    tag: str = "",
):
    """
    Gather tensor data across from all machines and concatenate over ``gather_dim``.

    Note that it currently only supports gather_dim = 0.

    This function is the same as all_gather_tensor but will propagate the
    backwards gradient across workers.

    See all_gather_tensor for more details on usage.
    """
    group = _resolve_group(group, tag)
    group_size = c10d._get_group_size_by_name(group)

    tensor = torch.ops._c10d_functional_autograd.all_gather_into_tensor(
        self, group_size, _group_or_group_name(group)
    )
    res = _FromTorchTensor.apply(tensor)
    if gather_dim != 0:
        # Check if _maybe_view_chunk_cat can use the view optimization.
        # If not, it will use torch.cat which needs the data anyway, so
        # wait early to avoid AsyncCollectiveTensor dispatch overhead.
        if isinstance(res, AsyncCollectiveTensor):
            shape = list(res.shape)
            numel_between = math.prod(shape[1:gather_dim]) if gather_dim > 1 else 1
            can_use_view = shape[0] == group_size and numel_between == 1
            if not can_use_view:
                res = res.wait()
        res = _maybe_view_chunk_cat(res, group_size, gather_dim)
    return res

