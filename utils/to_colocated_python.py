
def to_colocated_python(input_tree: PyTree) -> PyTree:
  """Copies a pytree of arrays to colocated CPU devices."""

  def _get_sharding(x: Any) -> jax.sharding.Sharding | None:
    if isinstance(x, jax.Array):
      cpu_sharding = colocated_cpu_sharding(x.sharding)
      logging.vlog(
          2,
          'Staging array from %s to colocated CPU sharding %s',
          x.sharding,
          cpu_sharding,
      )
      return cpu_sharding
    return None

  cpu_sharding_tree = jax.tree.map(_get_sharding, input_tree)
  return jax.device_put(input_tree, cpu_sharding_tree, may_alias=True)

