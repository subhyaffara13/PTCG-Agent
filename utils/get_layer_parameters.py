
def get_layer_parameters(layer: nn.Module) -> nn.Param:
  """Filter to get the model's BatchNorm stats."""

  return nn.state(layer, nn.Param)

