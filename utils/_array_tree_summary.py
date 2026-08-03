import math


def _array_tree_summary(tree: PyTree) -> str:
  """Returns a compact shape/dtype-only summary without materializing arrays.

  Non-array leaves are ignored because this helper is only used for debug
  logging. Save-path validation happens outside logging-gated code.

  Args:
    tree: The PyTree payload block to summarize.

  Returns:
    A compact shape/dtype-only summary wrapper.
  """
  array_leaves = [
      leaf for leaf in jax.tree.leaves(tree) if isinstance(leaf, jax.Array)
  ]
  total_bytes = 0
  platforms = set()
  samples = []
  for leaf in array_leaves:
    total_bytes += math.prod(leaf.shape) * leaf.dtype.itemsize
    platforms.update(device.platform for device in leaf.sharding.device_set)
    if len(samples) < 3:
      samples.append(
          f'shape={leaf.shape}, dtype={leaf.dtype}, '
          f'sharding={type(leaf.sharding).__name__}'
      )
  gib = total_bytes / (1024**3)
  return (
      f'array_leaves={len(array_leaves)}, estimated_bytes={total_bytes} '
      f'({gib:.2f} GiB), platforms={sorted(platforms)}, '
      f'samples={samples}'
  )

