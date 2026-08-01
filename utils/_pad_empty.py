
def _pad_empty(array: Array, pad_width: PadValue[int]) -> Array:
  # Note: jax.numpy.empty = jax.numpy.zeros
  for i in range(np.ndim(array)):
    shape_before = array.shape[:i] + (pad_width[i][0],) + array.shape[i + 1:]
    pad_before = array_creation.empty_like(array, shape=shape_before)

    shape_after = array.shape[:i] + (pad_width[i][1],) + array.shape[i + 1:]
    pad_after = array_creation.empty_like(array, shape=shape_after)
    array = lax.concatenate([pad_before, array, pad_after], dimension=i)
  return array

