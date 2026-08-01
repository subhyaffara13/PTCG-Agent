
def _roll_dynamic(a: Array, shift: Array, axis: Sequence[int]) -> Array:
  b_shape = lax.broadcast_shapes(shift.shape, np.shape(axis))
  if len(b_shape) != 1:
    msg = "'shift' and 'axis' arguments to roll must be scalars or 1D arrays"
    raise ValueError(msg)

  for x, i in zip(broadcast_to(shift, b_shape),
                  np.broadcast_to(axis, b_shape)):  # pyrefly: ignore[no-matching-overload]
    a_shape_i = array(a.shape[i], dtype=np.int32)
    x = ufuncs.remainder(lax.convert_element_type(x, np.int32),
                         lax.max(a_shape_i, np.int32(1)))
    a_concat = lax.concatenate((a, a), i)
    a = lax_slicing.dynamic_slice_in_dim(a_concat, a_shape_i - x, a.shape[i], axis=i)
  return a

