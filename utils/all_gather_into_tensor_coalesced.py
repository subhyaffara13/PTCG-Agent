
def all_gather_into_tensor_coalesced(
    self: list[torch.Tensor], group: RANK_TYPES, tag: str = ""
) -> list[torch.Tensor]:
    """
    Gather a list of tensors across from all machines.

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
    tensor_list = torch.ops._c10d_functional.all_gather_into_tensor_coalesced(  # type: ignore[attr-defined]
        self,
        group_size,
        _group_or_group_name(group),
    )
    return list(map(_maybe_wrap_tensor, tensor_list))

