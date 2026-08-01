
def _all_to_all_roofline(
  ctx: roofline.RooflineRuleContext,
  *args,
  axis_name: tuple[str, ...],
  **kw,
) -> roofline.RooflineResult:
  if zeros_result := _return_zeros_if_one_sized_axis(ctx, axis_name):
    return zeros_result

  assert ctx.mesh
  mesh = ctx.mesh.shape
  size = roofline.RooflineShape.total_bytes(ctx.avals_in) * np.prod([
    mesh[axis] for axis in axis_name
  ])

  smallest_axis = sorted(axis_name, key=lambda x: mesh[x])[0]
  num_axes = len(axis_name)
  bisection_bw = mesh[smallest_axis] ** (num_axes - 1)
  if mesh[smallest_axis] > 2:
    # Times 2 because of wraparound.
    bisection_bw *= 2

  # Half the data needs to cross the bisection on average.
  ici_bytes = size / 2 / bisection_bw

  # The latency is the max number of hops across the mesh.
  ici_latency = sum(mesh[axis] / 2 for axis in axis_name)

  return roofline.RooflineResult(
    ici_bytes={axis: int(ici_bytes) for axis in axis_name},
    ici_latency={axis: int(ici_latency) for axis in axis_name},
  )

