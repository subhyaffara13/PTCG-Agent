
def _get_layouts_from_executable(
    xla_executable, in_layouts, out_layouts, num_ordered_effects, in_avals,
    out_avals) -> tuple[Sequence[Layout | None], Sequence[Layout | None]]:
  try:
    in_layouts_xla = xla_executable.get_parameter_layouts()
    out_layouts_xla = xla_executable.get_output_layouts()
  except:
    return (None,) * len(in_layouts), (None,) * len(out_layouts)

  if num_ordered_effects > 0:
    in_layouts_xla = in_layouts_xla[num_ordered_effects:]
    out_layouts_xla = out_layouts_xla[num_ordered_effects:]

  new_in_layouts = []
  for x, l, aval in safe_zip(in_layouts_xla, in_layouts, in_avals):
    x = Layout.from_pjrt_layout(x)
    if isinstance(l, Layout) and not is_user_xla_layout_equal(l, x):
      raise AssertionError(
          f"Unexpected XLA layout override: (XLA) {x} != {l} "
          f"(User input layout) for type={aval.str_short()}")
    # Always append the XLA layout because it has the full information
    # (tiling, etc) even if the user layout does not specify tiling.
    new_in_layouts.append(x)

  new_out_layouts = []
  for x, l, aval in safe_zip(out_layouts_xla, out_layouts, out_avals):
    x = Layout.from_pjrt_layout(x)
    if isinstance(l, Layout) and not is_user_xla_layout_equal(l, x):
      raise AssertionError(
          f"Unexpected XLA layout override: (XLA) {x} != {l} "
          f"(User output layout) for type={aval.str_short()}")
    # Always append the XLA layout because it has the full information
    # (tiling, etc) even if the user layout does not specify tiling.
    new_out_layouts.append(x)

  assert all(isinstance(i, Layout) for i in new_in_layouts)
  assert all(isinstance(o, Layout) for o in new_out_layouts)
  return new_in_layouts, new_out_layouts

