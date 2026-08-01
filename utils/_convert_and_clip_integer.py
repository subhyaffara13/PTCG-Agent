
def _convert_and_clip_integer(val: Array, dtype: DType) -> Array:
  """
  Convert integer-typed val to specified integer dtype, clipping to dtype
  range rather than wrapping.

  Args:
    val: value to be converted
    dtype: dtype of output

  Returns:
    equivalent of val in new dtype

  Examples
  --------
  Normal integer type conversion will wrap:

  >>> val = jnp.uint32(0xFFFFFFFF)
  >>> val.astype('int32')
  Array(-1, dtype=int32)

  This function clips to the values representable in the new type:

  >>> _convert_and_clip_integer(val, 'int32')
  Array(2147483647, dtype=int32)
  """
  assert isinstance(val, Array)
  if not (dtypes.issubdtype(dtype, np.integer) and dtypes.issubdtype(val.dtype, np.integer)):
    raise TypeError("_convert_and_clip_integer only accepts integer dtypes.")

  min_val = lax._const(val, max(dtypes.iinfo(dtype).min,
                                dtypes.iinfo(val.dtype).min))
  max_val = lax._const(val, min(dtypes.iinfo(dtype).max,
                                 dtypes.iinfo(val.dtype).max))
  return jnp.clip(val, min_val, max_val).astype(dtype)

