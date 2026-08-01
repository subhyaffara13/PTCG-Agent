
def _reduce_window_min(operand: Array, window_dimensions: core.Shape,
                       window_strides: Sequence[int],
                       padding: Sequence[tuple[int, int]],
                       base_dilation: Sequence[int] | None = None,
                       window_dilation: Sequence[int] | None = None) -> Array:
  if base_dilation is None:
    base_dilation = (1,) * len(window_dimensions)
  if window_dilation is None:
    window_dilation = (1,) * len(window_dimensions)
  return reduce_window_min_p.bind(
      operand, window_dimensions=tuple(window_dimensions),
      window_strides=tuple(window_strides), padding=tuple(padding),
      base_dilation=tuple(base_dilation),
      window_dilation=tuple(window_dilation))

