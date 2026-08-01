
def is_user_xla_layout_equal(ul: Layout | AutoLayoutSingleton,
                             xl: Layout) -> bool:
  if isinstance(ul, Layout) and not ul.tiling:
    return ul.major_to_minor == xl.major_to_minor
  else:
    return ul == xl

