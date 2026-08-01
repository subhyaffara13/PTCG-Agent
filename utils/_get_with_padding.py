
def _get_with_padding(
    x: np.ndarray, uninitialized_memory: Literal['nan', 'zero']
) -> np.ndarray:
  padded_shape = _get_padded_shape(x.shape, x.dtype)
  uninitialized_value = interpret_utils.get_uninitialized_value(
      x.dtype, uninitialized_memory
  )
  result = np.full(padded_shape, uninitialized_value, x.dtype)
  result[tuple(slice(0, dim) for dim in x.shape)] = x
  return result

