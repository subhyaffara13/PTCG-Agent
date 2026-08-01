
def _resolve_out_layouts(out_layouts, out_shardings, out_avals):
  new_out_layouts = []
  for out_l, out_s, out_aval in safe_zip(out_layouts, out_shardings, out_avals):
    if out_l is None:
      new_out_layouts.append(None)
    elif (isinstance(out_l, Layout) and
          pxla.is_default_layout(out_l, out_s, out_aval)):
      new_out_layouts.append(None)
    else:
      new_out_layouts.append(out_l)
  return tuple(new_out_layouts)

