
def assert_specs_on_allowed_cpu_ids(
    tree: PyTree,
    *,
    allowed_ids: frozenset[int],
    tree_name: str,
) -> None:
  """Validates ShapeDtypeStruct leaves reference only expected CPU ids."""
  leaves = jax.tree.leaves(tree)
  spec_leaves = [x for x in leaves if isinstance(x, jax.ShapeDtypeStruct)]
  if not spec_leaves:
    return

  for i, spec in enumerate(spec_leaves):
    sharding = spec.sharding
    if sharding is None:
      raise ValueError(
          f'{tree_name} contains non-CPU or unexpected device ids. '
          f'First mismatch: (leaf={i}, sharding=None).'
      )
    platforms = sorted({d.platform for d in sharding.device_set})
    ids = {d.id for d in sharding.device_set}
    invalid = sorted(ids - allowed_ids)
    if platforms != ['cpu'] or invalid:
      sample_devices = sorted(sharding.device_set, key=lambda d: d.id)[:4]
      raise ValueError(
          f'{tree_name} contains non-CPU or unexpected device ids. '
          f'First mismatch: (leaf={i}, platforms={platforms}, '
          f'invalid_ids={invalid[:8]}, '
          f'sample_devices={[(d.id, d.platform) for d in sample_devices]}).'
      )

