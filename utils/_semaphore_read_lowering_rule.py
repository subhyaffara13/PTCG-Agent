
def _semaphore_read_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    args_tree,
):
  sem_aval, sem_transforms_avals = tree_util.tree_unflatten(args_tree, ctx.avals_in)
  primitives.check_sem_avals(
      sem_aval,
      sem_transforms_avals,
      "read",
      allowed_semaphore_types={
          tpu_core.dma_semaphore,
          pallas_core.semaphore,
          pallas_core.barrier_semaphore,
          pallas_core.SEMAPHORE_INTERPRET_DTYPE,
      },
  )
  sem, transforms = tree_util.tree_unflatten(args_tree, args)
  sem, _ = _transform_ref(sem, sem_aval, sem_aval.shape, transforms)
  return tpu.sem_read(sem)


def _semaphore_read_lowering_rule(ctx: LoweringRuleContext, *args, args_tree):
  sem, transforms = tree_util.tree_unflatten(args_tree, args)
  sem_aval, transform_avals = tree_util.tree_unflatten(args_tree, ctx.avals_in)
  assert isinstance(sem_aval, state_types.AbstractRef)
  sem, _, transforms = _handle_transforms(ctx, sem_aval, sem, transform_avals, transforms)
  if transforms:
    raise NotImplementedError(f"Unhandled transforms for semaphore_read: {transforms}")
  sem_ptr = mgpu.utils.memref_ptr(sem)
  i32_ty = ir.IntegerType.get_signless(32)
  result = llvm_dialect.inline_asm(
      i32_ty,
      [sem_ptr],
      "ld.acquire.sys.u32 $0,[$1];",
      "=r,l",
      has_side_effects=True,
  )
  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    return _ensure_fa(result, jnp.int32)
  return result

