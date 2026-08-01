
def _multimem_load_reduce_lowering_rule(
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
  if (layout := ctx.out_layout_hint) is None:
    raise RuntimeError(
        "Failed to infer the output layout of multimem_load_reduce. Please apply"
        " plgpu.layout_cast to its output right after its creation."
    )
  if not isinstance(layout, (mgpu.TiledLayout, mgpu.WGStridedFragLayout)):
    raise ValueError(
        "Only tiled and WG strided layouts are supported by"
        f" multimem_load_reduce, but got {layout}"
    )
  dtype = ctx.avals_out[0].dtype
  transforms = tree.unflatten(transforms_leaves)
  transform_avals = tree.unflatten(ctx.avals_in[1:])
  ref_aval = ctx.avals_in[0]
  assert isinstance(ref_aval, state_types.AbstractRef)
  ref, _, transforms = lowering._handle_transforms(ctx, ref_aval, ref,
                                                   transform_avals, transforms,
                                                   allow_peer_refs=False)
  if transforms:
    raise NotImplementedError(
        f"Unhandled transforms for multimem_load_reduce: {transforms}"
    )
  multi_ref = ctx.launch_ctx.to_remote_multicast(ref)
  is_signed = mgpu_utils.is_signed(dtype)
  arr = mgpu.FragmentedArray.load_reduce_untiled(
      multi_ref, layout=layout, is_signed=is_signed, reduction=reduction_op
  )
  return arr

