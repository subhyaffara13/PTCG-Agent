
def permute_tensor(
    self: torch.Tensor,
    src_dst: list[int],
    group: RANK_TYPES,
    tag: str = "",
) -> torch.Tensor:
    """
    Permutes the elements of the tensor according to the given source/destination pairs. `src_dst` should
    be defined such that src_dst[m] == n means m sends to n.

    Group can be one of:
        List[int]: ranks participating in the collective.
        List[List[int]]: 2D mesh of ranks taking part of this collective in MPMD.
        ProcessGroup: Will perform a collective using the ranks and tag of the PG.
        DeviceMesh: Do a SPMD collective over all ranks of the mesh
        (DeviceMesh, int): Do a MPMD collective over one
    """
    t, rankset, group_size = _expand_group(group, tag)
    local_pg = c10d._find_or_create_pg_by_ranks_and_tag(t, rankset, group_size)

    output_split_sizes = [0] * group_size
    input_split_sizes = [0] * group_size
    for src, dst in enumerate(src_dst):
        if src == dist.get_rank(local_pg):
            input_split_sizes[dst] = self.numel()
        if dst == dist.get_rank(local_pg):
            output_split_sizes[src] = self.numel()

    return all_to_all_single(self, output_split_sizes, input_split_sizes, group, tag)

