
def make_contiguous_for_perm(
    t: torch.Tensor,
    perm: list[int],
) -> torch.Tensor:
    """
    Restride `t` such that `t.permute(perm)` is contiguous.
    """
    inv_perm = [0] * len(perm)
    for i, p in enumerate(perm):
        inv_perm[p] = i
    return t.permute(perm).contiguous().permute(inv_perm)

