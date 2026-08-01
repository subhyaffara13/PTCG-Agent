
def flex_cp_allgather(
    k: torch.Tensor, v: torch.Tensor, seq_dim: int, pg_name: c10d.GroupName
) -> tuple[torch.Tensor, torch.Tensor]:
    k = k.contiguous()
    v = v.contiguous()
    k = funcol.all_gather_tensor(k, seq_dim, pg_name)
    v = funcol.all_gather_tensor(v, seq_dim, pg_name)
    if isinstance(k, funcol.AsyncCollectiveTensor):
        k = k.wait()
    if isinstance(v, funcol.AsyncCollectiveTensor):
        v = v.wait()
    return k, v

