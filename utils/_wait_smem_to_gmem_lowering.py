
def _wait_smem_to_gmem_lowering(
    ctx: lowering.LoweringRuleContext, n, *, wait_read_only
):
  if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    scope = mgpu_utils.ThreadSubset.WARP
  else:
    scope = mgpu_utils.ThreadSubset.WARPGROUP
  ctx.launch_ctx.await_async_copy(
      allow_groups=n, await_read_only=wait_read_only,
      scope=scope
  )
  return ()

