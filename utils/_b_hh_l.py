
def _b_hh_l(layer_i: int, input_size: int, hidden_size: int,
            bidirectional: bool) -> Shape:
  """Shape of b_hi|b_hf|b_hg|b_ho."""
  return (4 * hidden_size,)

