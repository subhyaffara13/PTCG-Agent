
def _convert_layout_for_lowering(
    aval: core.AbstractValue, layout: FfiLayoutOptions = None) -> Sequence[int]:
  """Convert a layout to the minor-to-major order used by the custom call API."""
  if layout is None:
    return tuple(reversed(range(len(_aval_shape(aval)))))
  elif isinstance(layout, Layout):
    if layout.tiling is not None:
      raise ValueError("The FFI does not support layouts with tiling")
    return layout.major_to_minor[::-1]
  else:
    return tuple(layout)

