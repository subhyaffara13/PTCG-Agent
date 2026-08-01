
def _shrink_mask_info_dkv(
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
  grouped_non_zero_rows = []
  # Group non-zero rows based on which column they belong to.
  for col_index in range(head_block_mask.shape[1]):
    col = head_block_mask[:, col_index]
    non_zero_rows = np.nonzero(col)[0]
    grouped_non_zero_rows.append(non_zero_rows)

  # Pad each col in the non-zero indices to match the height of the longest
  # col. This avoids having jagged cols.
  max_non_zero_rows = max(len(x) for x in grouped_non_zero_rows)
  padded_non_zero_rows_list = []
  padding = -1
  for col in grouped_non_zero_rows:
    padded_non_zero_rows_list.append(
        np.pad(
            col,
            pad_width=(max_non_zero_rows - col.shape[0], 0),
            constant_values=padding,
        )
    )

  padded_non_zero_rows = np.stack(padded_non_zero_rows_list, axis=1)

  assert padded_non_zero_rows.shape[1] == block_mask.shape[2], (
      padded_non_zero_rows.shape,
      block_mask.shape,
  )

  # For each col of array, select the rows indices in padded_non_zero_rows,
  # ignore padding.
  def select_rows(array):
    assert array.ndim == 2
    assert padded_non_zero_rows.ndim == 2
    assert array.shape[1] == padded_non_zero_rows.shape[1]
    assert array.shape[0] >= padded_non_zero_rows.shape[0]
    selected_cols = []
    for col in range(array.shape[1]):
      row = padded_non_zero_rows[:, col]
      selected = array[:, col][row]
      selected = np.where(row != padding, selected, 0)
      selected_cols.append(selected)

    return np.stack(selected_cols, axis=1)

  return _slice_mask_info(
      block_mask=block_mask,
      data_next=data_next,
      mask_next=mask_next,
      head_shards=head_shards,
      slice_function=select_rows,
  )

