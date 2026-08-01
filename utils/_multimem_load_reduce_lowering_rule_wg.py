
def _multimem_load_reduce_lowering_rule_wg(
    ctx: lowering.LoweringRuleContext, ref, *transforms_leaves, tree, collective_axes, reduction_op,
):
  if (mesh_info := ctx.module_ctx.mesh_info) is None:
    raise ValueError(
        "JAX device mesh is required by multimem_load_reduce, but not defined."
    )
  if set(collective_axes) != set(mesh_info.axis_names):
    raise NotImplementedError(
        "Only collective_axes that include all JAX device mesh"
        f" ({mesh_info.axis_names}) axes are supported, but got"
        f" {collective_axes}"
    )
  transforms = tree.unflatten(transforms_leaves)
  transform_avals = tree.unflatten(ctx.avals_in[1:])
  ref_aval = ctx.avals_in[0]
  assert isinstance(ref_aval, state_types.AbstractRef)
  ref, _, transforms = lowering._handle_transforms(ctx, ref_aval, ref,
                                                   transform_avals, transforms)
  if transforms:
    raise NotImplementedError(
        f"Unhandled transforms for multimem_load_reduce: {transforms}"
    )
  assert reduction_op is not None
  is_signed = mgpu_utils.is_signed(ref_aval.dtype)
  match reduction_op:
    case "min" if is_signed is None:
      reduction_op_attr = mgpu.dialect.MultimemLoadReductionType.Min
    case "min" if is_signed is True:
      reduction_op_attr = mgpu.dialect.MultimemLoadReductionType.Smin
    case "min" if is_signed is False:
      reduction_op_attr = mgpu.dialect.MultimemLoadReductionType.Umin
    case "max" if is_signed is True:
      reduction_op_attr = mgpu.dialect.MultimemLoadReductionType.Smax
    case "max" if is_signed is False:
      reduction_op_attr = mgpu.dialect.MultimemLoadReductionType.Umax
    case "max" if is_signed is None:
      reduction_op_attr = mgpu.dialect.MultimemLoadReductionType.Max
    case "add":
      reduction_op_attr = mgpu.dialect.MultimemLoadReductionType.Add
    case "and":
      reduction_op_attr = mgpu.dialect.MultimemLoadReductionType.And
    case "or":
      reduction_op_attr = mgpu.dialect.MultimemLoadReductionType.Or
    case "xor":
      reduction_op_attr = mgpu.dialect.MultimemLoadReductionType.Xor
    case _:
      raise ValueError(f"Unsupported integer reduction op: {reduction_op}")

  multimem_ref = ctx.launch_ctx.to_remote_multicast(ref)
  return mgpu.dialect.multimem_load_reduce(
      source=multimem_ref.ref,
      reduction_type=reduction_op_attr,
  )

