
def assert_tree_is_sharded(tree: ArrayTree,
                           *,
                           devices: Sequence[pytypes.Device]) -> None:
  """Checks that all leaves are ndarrays sharded across the specified devices.

  Args:
    tree: A tree to assert.
    devices: A list of devices which the tree's leaves are expected to be
      sharded across. This list is order-sensitive.

  Raises:
    AssertionError: If the tree contains a leaf that is not a device array
      sharded across the specified devices.
  """
  assert_tree_has_only_ndarrays(tree)

  errors = []
  devices = tuple(devices)

  def _assert_fn(path, leaf):
    if leaf is not None:
      # Check that the leaf is a ShardedArray.
      if isinstance(leaf, jax.Array):
        if _check_sharding(leaf):
          shards = tuple(shard.device for shard in leaf.addressable_shards)
          if shards != devices:
            errors.append(
                f"Tree leaf '{_ai.format_tree_path(path)}' is sharded "
                f"across {shards} devices, expected {devices}."
            )
        else:
          errors.append(
              f"Tree leaf '{_ai.format_tree_path(path)}' is not sharded"
              f" (devices={leaf.devices()})."
          )
      else:
        errors.append(
            f"Tree leaf '{_ai.format_tree_path(path)}' is not a "
            f"jax.Array (type={type(leaf)})."
        )

  for path, leaf in jax.tree_util.tree_flatten_with_path(tree)[0]:
    _assert_fn(_ai.convert_jax_path_to_dm_path(path), leaf)
  if errors:
    raise AssertionError("\n".join(errors))

