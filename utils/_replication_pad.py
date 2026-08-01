
def _replication_pad(a: Tensor, padding: tuple[int, ...]) -> Tensor:
    def idx(left, middle, right):
        dim_idx = torch.arange(-left, middle + right, device=a.device)
        return torch.clamp(dim_idx, 0, middle - 1)

    return _reflection_or_replication_pad(
        a,
        padding,
        idx,
    )

