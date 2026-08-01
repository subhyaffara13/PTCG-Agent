
def _W_hh_l(layer_i: int, input_size: int, hidden_size: int,
            bidirectional: bool) -> Shape:
  """Shape of W_hi|W_hf|W_hg|W_ho."""
  return (4 * hidden_size, hidden_size)

