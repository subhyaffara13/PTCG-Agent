
def _tri(dtype: DTypeLike, shape: Shape, offset: DimSize) -> Array:
  """Like numpy.tri, create a 2D array with ones below a diagonal."""
  offset = asarray(core.dimension_as_value(offset))
  if not dtypes.issubdtype(offset.dtype, np.integer):
    raise TypeError(f"offset must be an integer, got {offset!r}")
  shape_dtype = lax_utils.int_dtype_for_shape(shape, signed=True)
  if (
      np.iinfo(offset.dtype).min < np.iinfo(shape_dtype).min
      or np.iinfo(offset.dtype).max > np.iinfo(shape_dtype).max
  ):
    shape_dtype = np.dtype(np.int64)
  dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "tri")
  bool_tri = ge(add(broadcasted_iota(shape_dtype, shape, 0),
                    offset.astype(shape_dtype)),
                broadcasted_iota(shape_dtype, shape, 1))
  return convert_element_type_p.bind(bool_tri, new_dtype=dtype, weak_type=False,
                                     sharding=None)

