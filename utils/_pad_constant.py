
def _pad_constant(array: Array, pad_width: PadValue[int], constant_values: Array) -> Array:
  nd = np.ndim(array)
  constant_values = lax._convert_element_type(
      constant_values, array.dtype, dtypes.is_weakly_typed(array))
  constant_values_nd = np.ndim(constant_values)

  if constant_values_nd == 0:
    widths = [(low, high, 0) for (low, high) in pad_width]
    return lax.pad(array, constant_values, widths)

  if constant_values_nd == 1:
    if constant_values.shape[-1] == 1:
      widths = [(low, high, 0) for (low, high) in pad_width]
      return lax.pad(array, squeeze(constant_values), widths)
    elif constant_values.shape[-1] != 2:
      raise ValueError("jnp.pad: constant_values has unsupported shape "
                      f"{constant_values.shape}. If the shape is 1D or 2D, the "
                      "last dimension must be of size 1 or 2.")

  constant_values = broadcast_to(constant_values, (nd, 2))
  for i in range(nd):
    widths = [(0, 0, 0)] * nd
    if pad_width[i][0] != 0:
      widths[i] = (pad_width[i][0], 0, 0)
      array = lax.pad(array, constant_values[i, 0], widths)
    if pad_width[i][1] != 0:
      widths[i] = (0, pad_width[i][1], 0)
      array = lax.pad(array, constant_values[i, 1], widths)
  return array

