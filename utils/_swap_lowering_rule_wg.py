
def _swap_lowering_rule_wg(
    ctx: LoweringRuleContext, x_smem, value, *leaves, tree
):
  shape = ctx.avals_out[0].shape
  if shape and not isinstance(value.type, ir.VectorType):
    raise TypeError(f"Can only store scalars or vectors (got {value}).")
  if not (
      isinstance(x_smem, ir.Value) and isinstance(x_smem.type, ir.MemRefType)
  ):
    raise TypeError(f"Can only store to references (got {x_smem}).")
  if shape and ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    raise NotImplementedError("Can only store scalars in warp-level lowering.")
  transforms = jax.tree.unflatten(tree, leaves)
  transform_avals = jax.tree.unflatten(tree, ctx.avals_in[2:])
  assert isinstance(ctx.avals_in[0], state_types.AbstractRef)
  x_smem, _, transforms = _handle_transforms(
      ctx, ctx.avals_in[0], x_smem, transform_avals, transforms,
      allow_peer_refs=True
  )
  if transforms:
    raise NotImplementedError(
        "Transforms are not yet implemented for warpgroup semantics"
    )
  assert isinstance(x_smem, ir.Value)
  value = _ensure_ir_value(value, ctx.avals_in[1].dtype)
  if shape:
    old_value = mgpu.dialect.vector_load(x_smem)
    mgpu.dialect.vector_store(value, x_smem)
  else:
    old_value = memref_dialect.load(x_smem, [])
    memref_dialect.store(value, x_smem, [])
  return old_value

