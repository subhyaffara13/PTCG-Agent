
def shape_and_dtype_jax_array(a) -> tuple[Sequence[int | None], DType]:
  """Returns the shape and dtype of a jax.Array or a j"""
  if isinstance(a, api.ShapeDtypeStruct):
    return a.shape, a.dtype
  aval = core.typeof(a)
  return aval.shape, aval.dtype


def shape_and_dtype_jax_array(a) -> tuple[Sequence[int | None], DType]:
  """Returns the shape and dtype of a jax.Array or a j"""
  if isinstance(a, api.ShapeDtypeStruct):
    return a.shape, a.dtype
  aval = core.typeof(a)
  return aval.shape, aval.dtype

