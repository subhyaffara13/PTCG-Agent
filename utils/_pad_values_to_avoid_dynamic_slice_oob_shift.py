
def _pad_values_to_avoid_dynamic_slice_oob_shift(value,
                                   slice_sizes, unpad=False):
  """
  DynamicSlice and DynamicUpdateSlice adjust the start index in cases where the
  requested slice overruns the bounds of the array. This pads the array with
  uninitialised values such that the requested slice will never overrun.

  For example, if arr is [1.,2.,3.,4.] and a slice of size 4, start index 2 is
  requested then the result will be [3.,4.,NaN,NaN] after padding, rather than
  [1.,2.,3.,4.] from the unpadded array

  unpad=True performs the inverse operation
  """

  padding_config = tuple((0, slice_size, 0) for slice_size in slice_sizes)
  if unpad:
    padding_config = tuple((-low, -high, -interior)
                           for (low, high, interior) in padding_config)
  padding_value = uninitialized_value(shape=(), dtype=value.dtype)
  value = lax.pad(value,
                  padding_config=padding_config,
                  padding_value=padding_value)
  return value

