
def bucketize_scalar(
    self: torch.types.Number,
    boundaries: torch.Tensor,
    *,
    out_int32: bool = False,
    right: bool = False,
) -> torch.Tensor:
    return aten.bucketize(
        torch.tensor([self], device=boundaries.device),
        boundaries,
        out_int32=out_int32,
        right=right,
    ).squeeze(0)

