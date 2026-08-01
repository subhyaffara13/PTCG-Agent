
def _up_and_broadcast(doit):
  def up_and_broadcast(*args):
    broadcasted_shape = broadcast_shapes(*(a.shape for a in args))
    args = [broadcast_in_dim(a, broadcasted_shape, list(range(a.ndim))) for a in args]

    a_dtype = args[0].dtype
    needs_upcast = a_dtype == dtypes.bfloat16 or a_dtype == np.float16
    if needs_upcast:
      args = [convert_element_type(a, np.float32) for a in args]
      a_x_type = np.float32
    else:
      a_x_type = a_dtype
    result = doit(*args, dtype=a_x_type)
    if needs_upcast:
      result = convert_element_type(result, a_dtype)
    return result
  return up_and_broadcast

