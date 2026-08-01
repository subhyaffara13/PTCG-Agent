
def _multimem_store_lowering_rule(
    ctx: lowering.LoweringRuleContext, value, local_ref, *transforms_leaves, transforms_tree, collective_axes,
):
  if (mesh_info := ctx.module_ctx.mesh_info) is None:
    raise ValueError(
        "JAX device mesh is required by multimem_store, but not defined."
    )
  if set(collective_axes) != set(mesh_info.axis_names):
    raise NotImplementedError(
        "Only collective_axes that include all JAX device mesh"
        f" ({mesh_info.axis_names}) axes are supported, but got"
        f" {collective_axes}"
    )
  if transforms_tree is not None:
    transforms = tree_util.tree_unflatten(transforms_tree, transforms_leaves)
    local_ref_aval = ctx.avals_in[1]
    assert isinstance(local_ref_aval, state_types.AbstractRef)
    transform_avals = transforms_tree.unflatten(ctx.avals_in[2:])
    local_ref, _, transforms = lowering._handle_transforms(
        ctx, local_ref_aval, local_ref, transform_avals, transforms, allow_peer_refs=False
    )
    if transforms:
      raise NotImplementedError(
          f"Unhandled transforms for multimem_store: {transforms}"
      )
  multi_ref = ctx.launch_ctx.to_remote_multicast(local_ref)
  scalar = not ctx.avals_in[0].shape
  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
    val = lowering._ensure_ir_value(value, ctx.avals_in[0].dtype)
    if scalar:
      with lowering._wrap_in_custom_primitive_if_wg(ctx, [multi_ref.ref, val]) as [multi_ref, val]:
        mgpu_utils.MultimemRef(multi_ref).store(val, indices=[])
        if ctx.module_ctx.auto_barriers:
          mgpu.warpgroup_barrier()
    else:
      mgpu.dialect.vector_store(val, multi_ref.ref, optimized=False, multimem=True)
    return ()

  if scalar:
    multi_ref.store(lowering._ensure_ir_value(value, ctx.avals_in[0].dtype), [])
  else:
    value.store_untiled(multi_ref, optimized=False)
  if ctx.module_ctx.auto_barriers:
    mgpu.warpgroup_barrier()  # Make sure the writes have completed.
  return ()

