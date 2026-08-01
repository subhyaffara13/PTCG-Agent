
def _linear_indices_and_weights(coordinate: Array) -> list[tuple[Array, ArrayLike]]:
  lower = jnp.floor(coordinate)
  upper_weight = coordinate - lower
  lower_weight = 1 - upper_weight
  index = lower.astype(np.int32)
  return [(index, lower_weight), (index + 1, upper_weight)]

