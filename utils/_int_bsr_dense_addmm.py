
def _int_bsr_dense_addmm(
    input: torch.Tensor,
    bsr: torch.Tensor,
    dense: torch.Tensor,
    *,
    beta=1,
    alpha=1,
    left_alpha: torch.Tensor | None = None,
    right_alpha: torch.Tensor | None = None,
    out: torch.Tensor | None = None,
    skip_checks: bool = False,
    max_grid: tuple[int | None, int | None, int | None] | None = None,
    meta: dict | None = None,
):
    if out is None and dense.dtype is torch.int8:
        f_name = "_int_bsr_dense_addmm"
        crow_indices = bsr.crow_indices()
        batch_ndim = crow_indices.dim() - 1
        M = bsr.shape[batch_ndim]
        N = dense.shape[-1]
        original_batch_dims_broadcasted = broadcast_batch_dims(f_name, bsr, dense)
        out = torch.empty(
            original_batch_dims_broadcasted + (M, N),
            dtype=torch.int32,
            device=dense.device,
        )
    return bsr_dense_addmm(
        input,
        bsr,
        dense,
        beta=beta,
        alpha=alpha,
        left_alpha=left_alpha,
        right_alpha=right_alpha,
        out=out,
        skip_checks=skip_checks,
        max_grid=max_grid,
        meta=meta,
    )

