
def reduce_scatter_tensor_coalesced(
    inputs: list[torch.Tensor],
    reduceOp: str,
    scatter_dim: list[int],
    group: RANK_TYPES,
    tag: str = "",
) -> list[torch.Tensor]:
    """
    Reduces a list of tensors across all machines in such a way that all get
    the final result, then scatter the results to corresponding ranks.

    The input tensors are left unmodified.
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

    if len(scatter_dim) != len(inputs):
        raise AssertionError(
            f"Length of scatter_dim ({len(scatter_dim)}) must equal length of inputs ({len(inputs)})"
        )
    for idx, (dim, tensor) in enumerate(zip(scatter_dim, inputs)):
        if tensor.size(dim) % group_size != 0:
            raise AssertionError(
                f"input dimension {dim} ({tensor.size(dim)} must be a multiple of group_size {group_size} for tensor at index {idx}"
            )
        if dim != 0:
            tensor_list = torch.chunk(tensor, group_size, dim=dim)
            inputs[idx] = torch.cat(tensor_list)

    tensor_list = torch.ops._c10d_functional.reduce_scatter_tensor_coalesced(  # type: ignore[attr-defined]
        inputs,
        reduceOp.lower(),
        group_size,
        _group_or_group_name(group),
    )

    return list(map(_maybe_wrap_tensor, tensor_list))

