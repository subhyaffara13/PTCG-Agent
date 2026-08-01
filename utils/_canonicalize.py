
def _canonicalize(fx_g: fx.GraphModule) -> fx.GraphModule:
    for node in fx_g.graph.find_nodes(
        op="call_function", target=torch.ops.aten._to_copy
    ):
        node.target = torch.ops.aten.to
    fx_g.recompile()
    return fx_g


def _canonicalize(
    tree: Accumulator | AccumulationType | AccumulatorTree,
    num_microbatches: int | None,
) -> Accumulator:
  """Canonicalizes a PyTree of Accumulators/AccumulationTypes."""

  def fun(acc):
    if isinstance(acc, Accumulator):
      return acc
    match acc:
      case AccumulationType.MEAN:
        return _mean(num_microbatches)
      case AccumulationType.SUM:
        return _sum()
      case AccumulationType.RUNNING_MEAN:
        return _running_mean()
      case AccumulationType.CONCAT:
        return _concat(num_microbatches)
    raise ValueError(f'Unknown accumulator: {acc}')

  return _compose(jax.tree.map(fun, tree))

