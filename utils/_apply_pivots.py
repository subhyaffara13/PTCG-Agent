
def _apply_pivots(a, pivots, shape, *, inverse=False):
    perm = _pivots_to_permutation(pivots - 1, shape, inverse=inverse)

    if len(shape) == 1:
        return a[perm, :]
    else:
        idx = torch.meshgrid(
            *[torch.arange(s, device=a.device) for s in perm.shape], indexing="ij"
        )[:-1] + (perm, slice(None))
        return a[idx]

