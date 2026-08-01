
def get_dispatch_layouts(xla_in_layouts, in_shardings, in_avals):
  return [None if is_default_layout(l, s, a) else l
          for l, s, a, in safe_zip(xla_in_layouts, in_shardings, in_avals)]

