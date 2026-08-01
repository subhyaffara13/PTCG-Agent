
def _ragged_dot_mode_and_dim(
    lhs_rank: int, ragged_dot_dimension_numbers: RaggedDotDimensionNumbers
) -> tuple[RaggedDotMode, int]:
  assert len(ragged_dot_dimension_numbers.lhs_ragged_dimensions) == 1
  lhs_ragged_dim = ragged_dot_dimension_numbers.lhs_ragged_dimensions[0]
  (lhs_contracting, _), (lhs_batch, _) = ragged_dot_dimension_numbers.dot_dimension_numbers
  lhs_noncontracting = remaining(range(lhs_rank), lhs_contracting, lhs_batch)
  if lhs_ragged_dim in lhs_noncontracting:
    mode = RaggedDotMode.RAGGED_NONCONTRACTING
  elif lhs_ragged_dim in lhs_contracting:
    mode = RaggedDotMode.RAGGED_CONTRACTING
  elif lhs_ragged_dim in lhs_batch:
    mode = RaggedDotMode.RAGGED_BATCH
  else:
    raise TypeError(
        f'lhs_ragged_dim {lhs_ragged_dim} not found in '
        f'lhs_noncontracting {lhs_noncontracting}, '
        f'lhs_contracting {lhs_contracting}, or '
        f'lhs_batch {lhs_batch}.'
    )
  return mode, lhs_ragged_dim

