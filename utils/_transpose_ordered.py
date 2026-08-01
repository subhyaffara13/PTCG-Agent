
def _transpose_ordered(
    num_blocks_in_row: Tensor, col_indices: Tensor
) -> tuple[Tensor, Tensor]:
    dense = _ordered_to_dense(num_blocks_in_row, col_indices)
    return _dense_to_ordered(dense.transpose(-2, -1))

