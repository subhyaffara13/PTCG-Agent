
def scaled_dot_general_transpose_rhs(
    g, x, y, *, dimension_numbers, preferred_element_type: DTypeLike,
    configs: list[BlockScaleConfig]
  ):
  (x_contract, y_contract), (x_batch, y_batch) = dimension_numbers
  swapped_dimension_numbers = ((y_contract, x_contract), (y_batch, x_batch))
  y_bar = scaled_dot_general_transpose_lhs(
      g,
      y,
      x,
      dimension_numbers=swapped_dimension_numbers,
      preferred_element_type=preferred_element_type,
      configs=configs,
      swap_ans=True,
  )
  return y_bar

