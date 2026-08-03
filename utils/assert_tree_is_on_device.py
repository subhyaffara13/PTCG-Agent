from typing import Optional, Union

def assert_tree_is_on_device(tree: ArrayTree,
                             *,
                             platform: Union[Sequence[str],
                                             str] = ("gpu", "tpu"),
                             device: Optional[pytypes.Device] = None) -> None:
  """Checks that all leaves are ndarrays residing in device memory (in HBM).

  Sharded DeviceArrays are disallowed.

  Args:
    tree: A tree to assert.
    platform: A platform or a list of platforms where the leaves are expected to
      reside. Ignored if `device` is specified.
    device: An optional device where the tree's arrays are expected to reside.
      Any device (except CPU) is accepted if not specified.

  Raises:
    AssertionError: If the tree contains a leaf that is not an ndarray or does
      not reside on the specified device or platform.
  """
  assert_tree_has_only_ndarrays(tree)

  # If device is specified, require its platform.
  if device is not None:
    platform = (device.platform,)
  elif not isinstance(platform, collections.abc.Sequence):
    platform = (platform,)

  errors = []

  def _assert_fn(path, leaf):
    if leaf is not None:
      # Check that the leaf is a DeviceArray.
      if isinstance(leaf, jax.Array):
        if _check_sharding(leaf):
          errors.append((f"Tree leaf '{_ai.format_tree_path(path)}' is a "
                         f"ShardedDeviceArray which are disallowed. "
                         f" (type={type(leaf)})."))
        else:  # DeviceArray and not ShardedDeviceArray
          # Check the platform.
          leaf_device = list(leaf.devices())[0]
          if leaf_device.platform not in platform:
            errors.append((
                f"Tree leaf '{_ai.format_tree_path(path)}' resides on "
                f"'{leaf_device.platform}', expected '{platform}'."
            ))

          # Check the device.
          if device is not None and leaf.devices() != {device}:
            errors.append((
                f"Tree leaf '{_ai.format_tree_path(path)}' resides on "
                f"{leaf.devices()}, expected {device}."
            ))
      else:
        errors.append((f"Tree leaf '{_ai.format_tree_path(path)}' has "
                       f"unexpected type: {type(leaf)}."))

  for path, leaf in jax.tree_util.tree_flatten_with_path(tree)[0]:
    _assert_fn(_ai.convert_jax_path_to_dm_path(path), leaf)
  if errors:
    raise AssertionError("\n".join(errors))

