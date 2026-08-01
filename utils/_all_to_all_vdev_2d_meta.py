
def _all_to_all_vdev_2d_meta(
    input: torch.Tensor,
    out: torch.Tensor,
    in_splits: torch.Tensor,
    out_splits_offsets: torch.Tensor,
    group_name: c10d.GroupName,
    major_align: int | None = None,
) -> None:
    return None

