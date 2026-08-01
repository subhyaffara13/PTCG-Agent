
def _ppermute_roofline(
  ctx: roofline.RooflineRuleContext,
  *args,
  axis_name: tuple[str, ...],
  perm: tuple[tuple[int, int], ...],
  **kw,
) -> roofline.RooflineResult:
  if zeros_result := _return_zeros_if_one_sized_axis(ctx, axis_name):
    return zeros_result

  assert ctx.mesh
  mesh = ctx.mesh.shape
  mesh_dims: list[int] = [mesh.get(axis, 1) for axis in axis_name]
  shard_size = roofline.RooflineShape.total_bytes(ctx.avals_in)

  ici_contention: dict[tuple[tuple[int, ...], ...], float] = defaultdict(float)
  ici_latency = 0

  for src, dst in perm:
    if src == dst:
      continue
    # Perms are linearized.
    src_coords = tuple(int(i) for i in np.unravel_index(src, mesh_dims))
    dst_coords = tuple(int(i) for i in np.unravel_index(dst, mesh_dims))

    ici_latency_for_perm = 0

    # For each dimension.
    for i in range(len(axis_name)):
      dim_size = mesh_dims[i]
      src_pos = src_coords[i]
      dst_pos = dst_coords[i]

      if src_pos != dst_pos:
        # Calculate distance with wraparound.
        clockwise_dist = (dst_pos - src_pos) % dim_size
        counter_dist = (src_pos - dst_pos) % dim_size
        direction = 1 if clockwise_dist <= counter_dist else -1

        curr_pos = src_pos
        while curr_pos != dst_pos:
          curr_coords = util.tuple_update(src_coords, i, curr_pos)
          next_pos = (curr_pos + direction) % dim_size
          next_coords = util.tuple_update(curr_coords, i, next_pos)
          ici_contention[tuple(sorted([curr_coords, next_coords]))] += 1
          curr_pos = next_pos

        distance = min(clockwise_dist, counter_dist)
        ici_latency_for_perm += distance

    ici_latency = max(ici_latency, ici_latency_for_perm)

  ici_bytes = shard_size * max(ici_contention.values(), default=0)
  return roofline.RooflineResult(
    ici_bytes={axis: int(ici_bytes) for axis in axis_name},
    ici_latency={axis: int(ici_latency) for axis in axis_name},
  )

