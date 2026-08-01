
def _pow_jvp_lhs(g, ans, x, y):
  y_dtype = dtypes.dtype(y)
  result_dtype = dtypes.result_type(x, y)
  if result_dtype == bool:
    result_dtype = 'int32'
  x = convert_element_type(x, result_dtype)
  y = convert_element_type(y, result_dtype)
  if dtypes.issubdtype(y_dtype, np.integer):
    if x.shape != y.shape:
      shape = broadcast_shapes(x.shape, y.shape)
      sharding = broadcast_shardings(typeof(x), typeof(y))
      x = _maybe_broadcast(shape, x, sharding)
      y = _maybe_broadcast(shape, y, sharding)
    jac = select(eq(y, _const(y, 0)), _zeros(y),
                 mul(_replace_zero(y), pow(x, sub(y, _ones(y)))))
  else:
    jac = mul(y, pow(x, sub(y, _ones(y))))
  return mul(g, jac)

