
def _get_params_shapes_in_lstm(input_size: int, hidden_size: int,
                               num_layers: int,
                               bidirectional: bool) -> list[Shape]:
  """Get flat param shapes in LSTM. See module docstring for layout."""
  layer_shapes = []
  num_directions = 2 if bidirectional else 1
  num_pseudo_layers = num_layers * num_directions
  linear_weights = [_W_ih_l, _W_hh_l]
  for i in range(num_pseudo_layers):
    for w_kind in linear_weights:
      layer_shape = w_kind(i, input_size, hidden_size, bidirectional)
      layer_shapes.append(layer_shape)

  bias_weights = [_b_ih_l, _b_hh_l]
  for i in range(num_pseudo_layers):
    for w_kind in bias_weights:
      layer_shape = w_kind(i, input_size, hidden_size, bidirectional)
      layer_shapes.append(layer_shape)
  return layer_shapes

