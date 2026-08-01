
def _mgpu_async_prefetch_op_lowering_rule(
    ctx: LoweringContext, load_op: mgpu.AsyncPrefetchOp
) -> Sequence[ir.Value]:
  assert ctx.launch_context is not None

  gmem_slice, predicate = _gmem_slice_and_predicate(ctx, load_op)

  if load_op.collective:
    raise NotImplementedError("Collective prefetches are not supported yet.")

  ctx.launch_context.async_prefetch(
      gmem_ref=load_op.source,
      gmem_slice=gmem_slice,
      swizzle=None,
      gmem_transform=(),
      **predicate,  # pyrefly: ignore[bad-argument-type]
  )
  return []

