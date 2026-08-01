
def _pad_stats(array: Array, pad_width: PadValue[int],
               stat_length: PadValue[int] | None,
               stat_func: PadStatFunc) -> Array:
  nd = np.ndim(array)
  for i in range(nd):
    if stat_length is None:
      stat_before = stat_func(array, axis=i, keepdims=True)
      stat_after = stat_before
    else:
      array_length = array.shape[i]
      length_before, length_after = stat_length[i]
      if length_before == 0 or length_after == 0:
        raise ValueError("stat_length of 0 yields no value for padding")

      # Limit stat_length to length of array.
      length_before = min(length_before, array_length)
      length_after = min(length_after, array_length)

      slice_before = lax_slicing.slice_in_dim(array, 0, length_before, axis=i)
      slice_after = lax_slicing.slice_in_dim(array, -length_after, None, axis=i)
      stat_before = stat_func(slice_before, axis=i, keepdims=True)
      stat_after = stat_func(slice_after, axis=i, keepdims=True)

    if np.issubdtype(array.dtype, np.integer):
      stat_before = round(stat_before)
      stat_after = round(stat_after)

    stat_before = lax._convert_element_type(
        stat_before, array.dtype, dtypes.is_weakly_typed(array))
    stat_after = lax._convert_element_type(
        stat_after, array.dtype, dtypes.is_weakly_typed(array))

    npad_before, npad_after = pad_width[i]
    pad_before = repeat(stat_before, npad_before, axis=i)
    pad_after = repeat(stat_after, npad_after, axis=i)

    array = lax.concatenate([pad_before, array, pad_after], dimension=i)
  return array

