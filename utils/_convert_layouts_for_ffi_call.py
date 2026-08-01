
def _convert_layouts_for_ffi_call(
    avals: Sequence[core.AbstractValue],
    layouts: Sequence[FfiLayoutOptions]) -> tuple[Sequence[int], ...]:
  return tuple(
      _convert_layout_for_lowering(
          aval,
          layout if layout is None or isinstance(layout, Layout)
          else layout[::-1]
      )
      for aval, layout in zip(avals, layouts))

