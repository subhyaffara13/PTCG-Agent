
def _const(example, val):
  dtype = _dtype(example)
  if dtypes.is_weakly_typed_scalar(example):
    val = dtypes.scalar_type_of(example)(val)
    return val if dtype == _dtype(val) else np.array(val, dtype)
  return literals.TypedNdArray(np.array(val, dtype))

