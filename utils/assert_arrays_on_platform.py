
def assert_arrays_on_platform(
    tree: PyTree,
    *,
    expected_platform: str,
    tree_name: str,
) -> None:
  """Validates that all jax.Array leaves are on the expected platform."""
  leaves = jax.tree.leaves(tree)
  array_leaves = [x for x in leaves if isinstance(x, jax.Array)]
  if not array_leaves:
    return

  for i, leaf in enumerate(array_leaves):
    platforms = sorted({d.platform for d in leaf.sharding.device_set})
    if platforms != [expected_platform]:
      sample_devices = sorted(leaf.sharding.device_set, key=lambda d: d.id)[:4]
      raise ValueError(
          f'{tree_name} contains arrays not confined to '
          f'"{expected_platform}" devices. First mismatch: '
          f'(leaf={i}, platforms={platforms}, '
          f'sample_devices={[(d.id, d.platform) for d in sample_devices]}).'
      )

