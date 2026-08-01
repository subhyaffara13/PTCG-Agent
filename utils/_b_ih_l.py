
def _b_ih_l(layer_i: int, input_size: int, hidden_size: int,
            bidirectional: bool) -> Shape:
  """Shape of b_ii|b_if|b_ig|b_io."""
  return (4 * hidden_size,)

