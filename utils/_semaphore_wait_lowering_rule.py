
def _semaphore_wait_lowering_rule(ctx: LoweringRuleContext, *args, args_tree):
  sem_aval, _, _, _ = tree_util.tree_unflatten(args_tree, ctx.avals_in)
  sem, transforms, value, decrement = tree_util.tree_unflatten(args_tree, args)
  if not decrement:
    raise NotImplementedError("Non-decrementing wait is not supported.")
  sem, _ = _transform_ref(sem, sem_aval, sem_aval.shape, transforms)
  tpu.sem_wait(sem, value)
  return []


def _semaphore_wait_lowering_rule(
    ctx: lowering.LoweringRuleContext,
    *args,
    args_tree,
    memory_scope: Literal["sys", "gpu"] = "sys",
):
  sem, transforms, value, decrement = tree_util.tree_unflatten(args_tree, args)
  sem_aval, transform_avals, *_ = tree_util.tree_unflatten(
      args_tree, ctx.avals_in
  )
  assert isinstance(sem_aval, state_types.AbstractRef)
  sem, _, transforms = lowering._handle_transforms(ctx, sem_aval, sem, transform_avals, transforms)
  if transforms:
    raise NotImplementedError(
        f"Unhandled transforms for semaphore_wait: {transforms}"
    )
  val = lowering._ensure_ir_value(value, jnp.int32)

  scope = mgpu.ThreadSubset.WARPGROUP
  if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    scope = mgpu.ThreadSubset.WARP

  with lowering._wrap_in_custom_primitive_if_wg(ctx, [sem, val]) as [sem, val]:
    mgpu_utils.SemaphoreRef(mgpu.utils.memref_ptr(sem)).wait(
        val, decrement=decrement, scope=scope, memory_scope=memory_scope,
    )
  return ()

