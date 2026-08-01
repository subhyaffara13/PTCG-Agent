
def _is_ragged_contracting(
    lhs_rank: int, ragged_dot_dimension_numbers: RaggedDotDimensionNumbers
) -> bool:
  return (
      _ragged_dot_mode(lhs_rank, ragged_dot_dimension_numbers)
      == RaggedDotMode.RAGGED_CONTRACTING
  )

