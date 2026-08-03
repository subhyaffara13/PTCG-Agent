import math


def query_cluster_cancel_lowering(ctx: lowering.LoweringRuleContext,
                                  result_ref,
                                  *transforms_leaves,
                                  grid_names,
                                  transforms_tree):
  if transforms_tree is not None:
    res_transforms = transforms_tree.unflatten(transforms_leaves)
    result_aval = ctx.avals_in[0]
    assert isinstance(result_aval, state_types.AbstractRef)
    transform_avals = transforms_tree.unflatten(ctx.avals_in[1:])
    result_ref, _, res_transforms = lowering._handle_transforms(
        ctx, result_aval, result_ref, transform_avals, res_transforms)
    if res_transforms:
      raise NotImplementedError(
          f"Unimplemented transforms for result ref: {res_transforms}"
      )

  result_ty = ir.MemRefType(result_ref.type)
  bits = math.prod(result_ty.shape) * mgpu.bitwidth(result_ty.element_type)
  if bits != 128:
    raise TypeError(f"Response to decode must be 128 bits, but is {bits} bits.")

  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
    x, y, z, success = mgpu.dialect.query_cluster_cancel(result_ref)
  else:
    x, y, z, success = mgpu.query_cluster_cancel(result_ref)

  cta_grid = [x, y, z]
  i32 = ir.IntegerType.get_signless(32)
  # Divide out the cluster dimensions.
  for axis in ctx.module_ctx.axis_names.cluster:
    dim = lowering._resolve_cluster_axis(ctx.module_ctx.axis_names, axis)
    cta_grid[dim] = arith_dialect.divui(
        cta_grid[dim],
        mgpu.c(ctx.launch_ctx.cluster_size[dim], i32))
  # Convert to grid indices.
  requested_idxs = []
  for axis_name in grid_names:
    requested_idxs.append(lowering.block_id_to_grid_id(
        ctx, cta_grid, axis_name))
  return (*requested_idxs, success)

