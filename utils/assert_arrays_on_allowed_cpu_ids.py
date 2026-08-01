
def assert_arrays_on_allowed_cpu_ids(
    tree: PyTree,
    *,
    allowed_ids: frozenset[int],
    tree_name: str,
) -> None:
  """Validates that all array shardings use only expected CPU device ids."""
  leaves = jax.tree.leaves(tree)
  array_leaves = [x for x in leaves if isinstance(x, jax.Array)]
  if not array_leaves:
    return

  for i, leaf in enumerate(array_leaves):
    ids = {d.id for d in leaf.sharding.device_set}
    invalid = sorted(ids - allowed_ids)
    if invalid:
      sample_devices = sorted(leaf.sharding.device_set, key=lambda d: d.id)[:4]
      raise ValueError(
          f'{tree_name} contains unexpected CPU device ids. First mismatch: '
          f'(leaf={i}, invalid_ids={invalid[:8]}, '
          f'sample_devices={[(d.id, d.platform) for d in sample_devices]}).'
      )

