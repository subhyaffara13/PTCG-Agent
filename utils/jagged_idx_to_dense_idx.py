
def jagged_idx_to_dense_idx(
    jagged_idx,  # pyre-ignore[2]
    inverse_offsets_loader,  # pyre-ignore[2]
    offsets_loader,  # pyre-ignore[2]
    batch_size: int | sympy.Expr,
    max_seq_len: int | sympy.Expr,
    offsets_dtype: torch.dtype,
) -> tuple[sympy.Expr, sympy.Expr]:
    batch_idx = ops.indirect_indexing(
        inverse_offsets_loader([jagged_idx]),
        batch_size + 1,
    )
    batch_start = offsets_loader([batch_idx])
    seq = ops.index_expr(jagged_idx, offsets_dtype) - batch_start
    # check=False because there may be sequences longer than max_seq_len
    seq_idx = ops.indirect_indexing(seq, max_seq_len, check=False)
    return batch_idx, seq_idx

