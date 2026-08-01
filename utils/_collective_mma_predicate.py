
def _collective_mma_predicate(ctx: lowering.LoweringRuleContext,
                              collective_axis: str) -> ir.Value:
  """Computes a predicate to run only on the leader block."""
  cluster_axis = lowering._resolve_cluster_axis(
      ctx.module_ctx.axis_names, collective_axis)
  if cluster_axis != gpu_dialect.Dimension(0):
    # Note: resolve_cluster_axis checks if axis_names exists.
    assert ctx.module_ctx.axis_names is not None
    if len(ctx.module_ctx.axis_names.cluster) <= 1:
      raise ValueError("No cluster axes found.")
    minormost_cluster_axis = ctx.module_ctx.axis_names.cluster[0]
    raise ValueError(
        "Can only perform collective MMA along minormost cluster axis. "
        f"Got {collective_axis}, expected {minormost_cluster_axis}.")
  index = ir.IndexType.get()
  is_leader_block = arith_dialect.cmpi(
      arith_dialect.CmpIPredicate.eq,
      mgpu.utils.cluster_idx(cluster_axis), mgpu.c(0, index))
  return is_leader_block

