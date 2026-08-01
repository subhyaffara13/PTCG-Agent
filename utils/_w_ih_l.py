
def _W_ih_l(layer_i: int, input_size: int, hidden_size: int,
            bidirectional: bool) -> Shape:
  """Shape of W_ii|W_if|W_ig|W_io.

  Note that layer_i is an index of pseudo-layers.
  """
  if layer_i == 0 or (layer_i == 1 and bidirectional):
    return (4 * hidden_size, input_size)
  else:
    num_directions = 2 if bidirectional else 1
    return (4 * hidden_size, num_directions * hidden_size)

