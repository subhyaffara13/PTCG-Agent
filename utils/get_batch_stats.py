
def get_batch_stats(layer: nn.Module) -> nn.BatchStat:
  """Filter to get the model's parameters."""

  return nn.state(layer, nn.BatchStat)

