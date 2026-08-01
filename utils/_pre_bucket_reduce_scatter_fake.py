
def _pre_bucket_reduce_scatter_fake(
    rs_ins: list[torch.Tensor],
    group_size: int,
) -> torch.Tensor:
    out_numel = sum(rs_in.numel() for rs_in in rs_ins)
    return torch.empty((out_numel,), device=rs_ins[0].device, dtype=rs_ins[0].dtype)

