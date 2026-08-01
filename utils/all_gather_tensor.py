
def all_gather_tensor(
    self: torch.Tensor,
    gather_dim: int,
    group: RANK_TYPES,
    tag: str = "",
) -> torch.Tensor:
    """
    Gather tensor data across from all machines and concatenate over ``gather_dim``.

    Note that it currently only supports gather_dim = 0.

    The input tensor is left unmodified.
    Group can be one of:
        List[int]: ranks participating in the collective.
        List[List[int]]: 2D mesh of ranks taking part of this collective in MPMD.
        ProcessGroup: Will perform a collective using the ranks and tag of the PG.
        DeviceMesh: Do a SPMD collective over all ranks of the mesh
        (DeviceMesh, int): Do a MPMD collective over one dimension of the DeviceMesh

    :: N.B. If you pass a PG or a 1D list to perform a MPMD collective, the compiler won't be able to recover
    that information and perform collective algebraic optimization. Use other forms of input for that.
    """
    group = _resolve_group(group, tag)
    group_size = c10d._get_group_size_by_name(group)
    tensor = torch.ops._c10d_functional.all_gather_into_tensor(
        self, group_size, _group_or_group_name(group)
    )
    res = _maybe_wrap_tensor(tensor)
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

