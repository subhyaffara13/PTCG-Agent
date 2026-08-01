
def _scatter_lowering_rule(
    ctx: sc_lowering.LoweringRuleContext, *flat_args, tree, add
):
  ref, transforms, indices, x, mask = jax.tree.unflatten(tree, flat_args)
  ref_aval, *_ = tree.unflatten(ctx.avals_in)
  if isinstance(ref_aval.memory_space, pallas_core.CoreMemorySpace):
    if not isinstance(ref_aval.memory_space.mesh, sc_core.VectorSubcoreMesh):
      raise ValueError(
          "Scatter only supports VectorSubcoreMesh, got"
          f" {type(ref_aval.memory_space.mesh)}"
      )
    memory_space = ref_aval.memory_space.memory_space
  else:
    memory_space = ref_aval.memory_space
  if memory_space not in (
      tpu_core.MemorySpace.VMEM,
      pallas_core.MemorySpace.DEFAULT,
  ):
    raise ValueError(
        f"Scatter only supports storing to VMEM, got {memory_space}"
    )
  if transforms:
    ref_block_shape, *_ = ctx.block_shapes
    ref, _ = tc_lowering._transform_ref(
        ref, ref_aval, ref_block_shape, transforms
    )
  tpu.vector_store_idx(x, ref, indices, mask=mask, add=add)
  return ()

