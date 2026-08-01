
def _fused_all_gather_matmul_fallback(
    A_shard: torch.Tensor,
    Bs: list[torch.Tensor],
    gather_dim: int,
    group_name: c10d.GroupName,
    *,
    return_A: bool = True,
) -> tuple[torch.Tensor | None, list[torch.Tensor]]:
    group_size = c10d._get_group_size_by_name(group_name)
    A = torch.ops._c10d_functional.all_gather_into_tensor(
        A_shard.contiguous(), group_size, group_name
    )
    A = torch.ops._c10d_functional.wait_tensor(A)
    if gather_dim == A.ndim - 1 or gather_dim == -1:
        A_splits = A.chunk(group_size)
        A_mm = torch.cat(A_splits, dim=-1)
        res = [torch.matmul(A_mm, B) for B in Bs]
        if return_A:
            return A_mm, res
        else:
            return None, res

    A = A.view(group_size, *A_shard.shape).movedim(gather_dim + 1, 1).flatten(0, 1)
    res = [torch.matmul(A, B).movedim(0, gather_dim) for B in Bs]
    if return_A:
        return A.movedim(0, gather_dim), res
    else:
        return None, res

