
def _shrink_mask_info(
    *,
    block_mask: np.ndarray,
    data_next: np.ndarray,
    mask_next: np.ndarray | None,
    head_shards: int,
):
  assert block_mask.ndim == 3
  assert data_next.ndim == 3
  assert mask_next is None or mask_next.ndim == 3

  head_block_mask = block_mask[0]

  grouped_non_zero_cols = []
  # Group non-zero columns based on which row they belong to.
  for row_index in range(head_block_mask.shape[0]):
    head_block_mask_row = head_block_mask[row_index, :]
    non_zero_cols = np.nonzero(head_block_mask_row)[0]
    grouped_non_zero_cols.append(non_zero_cols)

  # Pad each row in the non-zero indices to match the width of the longest
  # row. This avoids having jagged rows.
  max_non_zero_cols = max(len(x) for x in grouped_non_zero_cols)
  padded_non_zero_cols_list = []
  padding = -1
  for row in grouped_non_zero_cols:
    padded_non_zero_cols_list.append(
        np.pad(
            row,
            pad_width=(0, max_non_zero_cols - row.shape[0]),
            constant_values=padding,
        )
    )

  padded_non_zero_cols = np.stack(padded_non_zero_cols_list, axis=0)

  assert padded_non_zero_cols.shape[0] == block_mask.shape[1], (
      padded_non_zero_cols.shape,
      block_mask.shape,
  )

  # For each row of array, select the columns indices in padded_non_zero_cols,
  # ignore padding.
  def select_cols(array):
    assert array.ndim == 2
    assert padded_non_zero_cols.ndim == 2
    assert array.shape[0] == padded_non_zero_cols.shape[0]
    assert array.shape[1] >= padded_non_zero_cols.shape[1]
    selected_rows = []
    for row in range(array.shape[0]):
      col = padded_non_zero_cols[row]
      selected = array[row][col]
      selected = np.where(col != padding, selected, 0)
      selected_rows.append(selected)

    return np.stack(selected_rows, axis=0)

  return _slice_mask_info(
      block_mask=block_mask,
      data_next=data_next,
      mask_next=mask_next,
      head_shards=head_shards,
      slice_function=select_cols,
  )

