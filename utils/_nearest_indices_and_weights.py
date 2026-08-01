
def _nearest_indices_and_weights(coordinate: Array) -> list[tuple[Array, ArrayLike]]:
  index = _round_half_away_from_zero(coordinate).astype(np.int32)
  weight = coordinate.dtype.type(1)
  return [(index, weight)]

