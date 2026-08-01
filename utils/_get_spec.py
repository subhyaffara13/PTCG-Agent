
def _get_spec(func: FunctionType) -> FunctionSpec:
    spec = _spec_cache.get(func)
    if spec is None:
        spec = FunctionSpec(func)
        _spec_cache[func] = spec
    return spec


def _get_spec(x: Any) -> api.ShapeDtypeStruct:
  """Extracts a spec for a value, which must be a JAX Array."""
  # TODO(hyeontaek): Allow Python values and automatically apply `shard_arg`
  # with a suitable sharding and layout.
  if not isinstance(x, jax.Array):
    raise ValueError(
        "colocated_python only supports jax.Array as input and output, but got"
        f" {type(x)}."
    )
  return api.ShapeDtypeStruct(shape=x.shape, dtype=x.dtype, sharding=x.sharding)

