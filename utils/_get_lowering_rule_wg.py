
def _get_lowering_rule_wg(
    ctx: LoweringRuleContext, x_ref, *leaves, tree, optimized=True
):
  if not isinstance(x_ref, ir.Value) and isinstance(x_ref, ir.MemRefType):
    raise TypeError(f"Can only load from references (got {x_ref}).")
  shape = ctx.avals_out[0].shape
  if shape and ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    raise ValueError("Can only load scalars in warp-level code.")

  transforms = jax.tree.unflatten(tree, leaves)
  assert isinstance(ctx.avals_in[0], state_types.AbstractRef)
  transform_avals = jax.tree.unflatten(tree, ctx.avals_in[1:])
  x_ref, _, transforms = _handle_transforms(
      ctx, ctx.avals_in[0], x_ref, transform_avals, transforms,
      allow_peer_refs=True
  )

  if transforms:
    raise NotImplementedError(
        "Transforms are not yet implemented for warpgroup semantics"
    )

  assert isinstance(x_ref, ir.Value)
  shape = ctx.avals_out[0].shape
  if shape:
    return mgpu.dialect.vector_load(x_ref, optimized=optimized)
  else:
    return memref_dialect.load(x_ref, [])

