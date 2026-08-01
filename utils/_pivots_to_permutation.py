
def _pivots_to_permutation(pivots, shape, *, inverse=False):
    perm = torch.empty(shape, dtype=torch.int32, device=pivots.device)
    perm[..., :] = torch.arange(shape[-1], dtype=torch.int32, device=pivots.device)
    indices = range(shape[-1])
    if inverse:
        indices = reversed(indices)

    if len(shape) > 1:
        for i in indices:
            j_s = pivots[..., i]
            perm_i = perm[..., i].clone()
            j_idx = torch.meshgrid(
                *[torch.arange(s, device=perm.device) for s in j_s.shape], indexing="ij"
            ) + (j_s,)
            perm_j = perm[j_idx]
            perm.index_put_(j_idx, perm_i)
            perm[..., i].copy_(perm_j)

    else:
        for i in indices:
            j = pivots[i]
            perm_i = perm[i].clone()
            perm_j = perm[j].clone()
            perm[i].copy_(perm_j)
            perm[j].copy_(perm_i)

    return perm

