
def _ring_collective_roofline(
  ctx: roofline.RooflineRuleContext,
  *args,
  axes: tuple[str, ...],
  is_reduce: bool = True,
  **kw,
) -> roofline.RooflineResult:
  if zeros_result := _return_zeros_if_one_sized_axis(ctx, axes):
    return zeros_result

  assert ctx.mesh
  mesh = ctx.mesh.shape
  current_shard_size = roofline.RooflineShape.total_bytes(ctx.avals_in)
  if is_reduce:
    current_shard_size /= np.prod([mesh[axis] for axis in axes])

  # We model the slowest color as the bottleneck.
  sorted_axes = sorted(axes, key=lambda x: mesh[x], reverse=True)
  num_axes = len(sorted_axes)

  ici_bytes = 0
  # Phase split.
  current_shard_size //= num_axes
  for axis in sorted_axes:
    axis_size = mesh[axis]
    # Do phase.
    ici_bytes += current_shard_size * (axis_size - 1)
    # Increase shard size.
    current_shard_size *= axis_size

  # Bottleneck is the longest axis.
  ici_latency = mesh[sorted_axes[0]] * num_axes

  return roofline.RooflineResult(
    ici_bytes={axis: int(ici_bytes) for axis in sorted_axes},
    ici_latency={axis: int(ici_latency) for axis in sorted_axes},
  )

