
def assert_tree_is_on_host(
    tree: ArrayTree,
    *,
    allow_cpu_device: bool = True,
    allow_sharded_arrays: bool = False,
) -> None:
  """Checks that all leaves are ndarrays residing in the host memory (on CPU).

  This assertion only accepts trees consisting of ndarrays.

  Args:
    tree: A tree to assert.
    allow_cpu_device: Whether to allow JAX arrays that reside on a CPU device.
    allow_sharded_arrays: Whether to allow sharded JAX arrays. Sharded arrays
      are considered "on host" only if they are sharded across CPU devices and
      `allow_cpu_device` is `True`.

  Raises:
    AssertionError: If the tree contains a leaf that is not an ndarray or does
      not reside on host.
  """
  assert_tree_has_only_ndarrays(tree)
  errors = []

  def _assert_fn(path, leaf):
    if leaf is not None:
      if not isinstance(leaf, np.ndarray):
        if isinstance(leaf, jax.Array):
          if _check_sharding(leaf):
            # Sharded array.
            if not allow_sharded_arrays:
              errors.append(
                  f"Tree leaf '{_ai.format_tree_path(path)}' is sharded and"
                  f" resides on {leaf.devices()} (sharded arrays are"
                  " disallowed)."
              )
            elif allow_cpu_device:
              if any(d.platform != "cpu" for d in leaf.devices()):
                errors.append(
                    f"Tree leaf '{_ai.format_tree_path(path)}' is sharded and"
                    f" resides on {leaf.devices()}."
                )
            else:
              errors.append(
                  f"Tree leaf '{_ai.format_tree_path(path)}' is sharded and"
                  f" resides on {leaf.devices()} (CPU devices are disallowed)."
              )
          elif allow_cpu_device:
            # Device array.
            leaf_device = list(leaf.devices())[0]
            if leaf_device.platform != "cpu":
              errors.append(
                  f"Tree leaf '{_ai.format_tree_path(path)}' resides"
                  f" on {leaf_device}."
              )
          else:
            errors.append((
                f"Tree leaf '{_ai.format_tree_path(path)}' resides "
                f"on {leaf.devices()} (CPU devices are disallowed)."
            ))
        else:
          # Not a jax.Array.
          errors.append((
              f"Tree leaf '{_ai.format_tree_path(path)}' has "
              f"unexpected type: {type(leaf)}."
          ))

  for path, leaf in jax.tree_util.tree_flatten_with_path(tree)[0]:
    _assert_fn(_ai.convert_jax_path_to_dm_path(path), leaf)
  if errors:
    raise AssertionError("\n".join(errors))

