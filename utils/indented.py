
def indented(subfigure: Any) -> figures_impl.TreescopeFigure:
  """Returns a figure object that displays a value with an indent.

  Args:
    subfigure: A value to render indented.
  """
  return figures_impl.TreescopeFigure(
      rendering_parts.indented_children([
          rendering_parts.vertical_space("0.25em"),
          treescope_part_from_display_object(subfigure),
          rendering_parts.vertical_space("0.25em"),
      ])
  )

