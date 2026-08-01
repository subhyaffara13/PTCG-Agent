
def _multimem_all_gather_matmul(
    A_shard: torch.Tensor,
    Bs: list[torch.Tensor],
    group_name: c10d.GroupName,
) -> list[torch.Tensor]:
    group = c10d._resolve_process_group(group_name)
    A_shape = torch.Size((A_shard.shape[0] * group.size(), *A_shard.shape[1:]))
    symm_mem = get_symm_mem_workspace(
        group_name, A_shape.numel() * A_shard.element_size()
    )
    A = symm_mem.get_buffer(symm_mem.rank, A_shape, A_shard.dtype)
    torch.ops.symm_mem.multimem_all_gather_out(A_shard, group_name, A)
    return [torch.matmul(A, B) for B in Bs]

