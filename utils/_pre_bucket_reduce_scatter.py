
def _pre_bucket_reduce_scatter(
    rs_ins: list[torch.Tensor],
    group_size: int,
) -> torch.Tensor:
    rs_ins_flattened = [x.view(group_size, -1) for x in rs_ins]
    new_rs_in = torch.cat(rs_ins_flattened, dim=1).flatten()
    return new_rs_in

