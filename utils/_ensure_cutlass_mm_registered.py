
def _ensure_cutlass_mm_registered():
    """Lazily register the cutlass_mm custom op.

    Registration is deferred to avoid importing torch.library at module load
    time, since torch.sparse is imported early during ``import torch``.
    """
    global _cutlass_mm_registered
    if _cutlass_mm_registered:
        return
    _cutlass_mm_registered = True

    from torch.library import custom_op

    @custom_op("semi_structured::cutlass_mm", mutates_args=())
    def cutlass_mm(
        dense: torch.Tensor,
        packed: torch.Tensor,
        meta: torch.Tensor,
        bias: torch.Tensor | None,
        out_features: int,
        min_rows: int,
        min_cols: int,
        should_transpose_dense: bool,
    ) -> torch.Tensor:
        m, n = dense.shape
        to_pad_m = (-m) % min_rows
        to_pad_n = (-n) % min_cols
        need_pad = to_pad_m != 0 or to_pad_n != 0
        dense_padded = dense
        if need_pad:
            dense_padded = torch.nn.functional.pad(dense, (0, to_pad_n, 0, to_pad_m))
        mm_input = dense_padded.t() if should_transpose_dense else dense_padded
        if bias is None:
            res = torch._sparse_semi_structured_mm(packed, meta, mm_input)
        else:
            res = torch._sparse_semi_structured_addmm(bias, packed, meta, mm_input)
        if need_pad:
            out_cols = m if should_transpose_dense else n
            return (
                res[:out_features]
                .narrow(1, 0, out_cols)
                .clone(memory_format=torch.contiguous_format)
            )
        return res.contiguous()

    @cutlass_mm.register_fake
    def _cutlass_mm_fake(
        dense: torch.Tensor,
        packed: torch.Tensor,
        meta: torch.Tensor,
        bias: torch.Tensor | None,
        out_features: int,
        min_rows: int,
        min_cols: int,
        transpose_dense: bool,
    ) -> torch.Tensor:
        out_cols = dense.shape[0] if transpose_dense else dense.shape[1]
        return torch.empty(
            out_features,
            out_cols,
            dtype=dense.dtype,
            device=dense.device,
        )

