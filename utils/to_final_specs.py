
def to_final_specs(
    input_tree: PyTree,
    tpu_or_cpu_specs: PyTree,
) -> PyTree:
  """Transfers jax.Arrays to the final sharding specs."""

  def _to_final_spec(leaf: Any, tpu_or_cpu_spec: Any) -> Any:
    if isinstance(leaf, jax.Array) and hasattr(tpu_or_cpu_spec, 'sharding'):
      logging.vlog(
          2,
          'Transferring array from %s to final sharding %s',
          leaf.sharding,
          tpu_or_cpu_spec.sharding,
      )
    return jax.device_put(leaf, tpu_or_cpu_spec.sharding, may_alias=True)

  return jax.tree.map(_to_final_spec, input_tree, tpu_or_cpu_specs)

