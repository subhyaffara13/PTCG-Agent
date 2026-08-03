import math


def _block_id(ctx: LoweringRuleContext, dim: gpu_dialect.Dimension) -> ir.Value:
  result = gpu_dialect.block_id(dim)
  cluster_size = ctx.launch_ctx.cluster_size
  if math.prod(cluster_size) == 1 or cluster_size[dim.value] == 1:
    return result
  # We scale the grid in the presence of clusters, so we need to scale the
  # block ID back here.
  return arith_dialect.divui(result, _as_index(cluster_size[dim.value]))

