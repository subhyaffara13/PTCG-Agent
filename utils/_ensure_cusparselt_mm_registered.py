
def _ensure_cusparselt_mm_registered():
    """Lazily register the cusparselt_mm custom op."""
    global _cusparselt_mm_registered
    if _cusparselt_mm_registered:
        return
    _cusparselt_mm_registered = True

    from torch.library import custom_op

    @custom_op("semi_structured::cusparselt_mm", mutates_args=())
    def cusparselt_mm(
        dense: torch.Tensor,
        packed: torch.Tensor,
        bias: torch.Tensor | None,
        out_features: int,
        min_rows: int,
        min_cols: int,
        fuse_transpose: bool,
        alg_id: int,
        should_transpose_dense: bool = False,
    ) -> torch.Tensor:
        m, n = dense.shape
        to_pad_m = (-m) % min_rows
        to_pad_n = (-n) % min_cols
        need_pad = to_pad_m != 0 or to_pad_n != 0
        dense_padded = dense
        if need_pad:
            dense_padded = torch.nn.functional.pad(dense, (0, to_pad_n, 0, to_pad_m))
        mm_input = dense_padded.t() if should_transpose_dense else dense_padded
        res = torch._cslt_sparse_mm(
            packed,
            mm_input,
            bias=bias,
            transpose_result=fuse_transpose,
            alg_id=alg_id,
        )
        if fuse_transpose:
            res = res.t()
        if need_pad:
            out_cols = m if should_transpose_dense else n
            return res.narrow(1, 0, out_cols).clone(
                memory_format=torch.contiguous_format
            )
        return res.contiguous()

    @cusparselt_mm.register_fake
    def _cusparselt_mm_fake(
        dense: torch.Tensor,
        packed: torch.Tensor,
        bias: torch.Tensor | None,
        out_features: int,
        min_rows: int,
        min_cols: int,
        fuse_transpose: bool,
        alg_id: int,
        should_transpose_dense: bool,
    ) -> torch.Tensor:
        out_cols = dense.shape[0] if should_transpose_dense else dense.shape[1]
        return torch.empty(
            out_features,
            out_cols,
            dtype=dense.dtype,
            device=dense.device,
        )

