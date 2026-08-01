
def get_num_params_in_lstm(input_size: int, hidden_size: int, num_layers: int,
                           bidirectional: bool) -> int:
  """Get param count in LSTM."""
  layer_shapes = _get_params_shapes_in_lstm(input_size, hidden_size, num_layers,
                                            bidirectional)
  param_count = sum(math.prod(shape) for shape in layer_shapes)
  return param_count

