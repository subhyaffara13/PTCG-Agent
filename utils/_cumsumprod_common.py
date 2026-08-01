
def _cumsumprod_common(
    func,
    init,
    a: TensorLikeType,
    dim: int,
    *,
    dtype: torch.dtype | None = None,
    out: Tensor | None = None,
) -> TensorLikeType:
    # We implement all the kwargs of a reduction. ATen just handles dtype
    # nb. This decomposition may not be as efficient as a backend-specific implementation
    ndim = a.ndim
    dim = utils.canonicalize_dim(ndim, dim)
    if ndim == 0:
        return func(a.unsqueeze(0), dim=0, dtype=dtype, out=out)
    a = a.unsqueeze(dim + 1)
    rg = torch.arange(a.shape[dim], device=a.device)
    mask = rg.unsqueeze(1) <= rg
    for _ in range(ndim - dim - 1):
        mask = mask.unsqueeze(-1)
    masked_a = torch.where(mask, a, init)
    return func(masked_a, dim=dim, dtype=dtype, out=out)

