
def _ragged_dot_mode(
    lhs_rank: int, ragged_dot_dimension_numbers: RaggedDotDimensionNumbers
) -> RaggedDotMode:
  return _ragged_dot_mode_and_dim(lhs_rank, ragged_dot_dimension_numbers)[0]

