
def _pad_wrap(array: Array, pad_width: PadValue[int]) -> Array:
  for i in range(np.ndim(array)):
    if array.shape[i] == 0:
      _check_no_padding(pad_width[i], "wrap")
      continue
    size = array.shape[i]
    left_repeats, left_remainder = divmod(pad_width[i][0], size)
    right_repeats, right_remainder = divmod(pad_width[i][1], size)
    total_repeats = left_repeats + right_repeats + 1
    parts = []
    if left_remainder > 0:
      parts += [lax_slicing.slice_in_dim(array, size - left_remainder, size, axis=i)]
    parts += total_repeats * [array]
    if right_remainder > 0:
      parts += [lax_slicing.slice_in_dim(array, 0, right_remainder, axis=i)]
    array = lax.concatenate(parts, dimension=i)
  return array

