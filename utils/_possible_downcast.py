
def _possible_downcast(x, example, spec):
  from jax._src.lax import lax as lax_internal  # pyrefly: ignore[missing-import]
  if (dtypes.issubdtype(x.dtype, np.complexfloating) and
      not dtypes.issubdtype(_dtype(example), np.complexfloating)):
    x = x.real
  dtype = _dtype(example)
  weak_type = dtypes.is_weakly_typed(example)
  sharding = NamedSharding(core.typeof(example).sharding.mesh, spec)
  return lax_internal._convert_element_type(
      x, dtype, weak_type, sharding=sharding)

