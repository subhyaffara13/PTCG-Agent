
def bolded(subfigure: Any) -> figures_impl.TreescopeFigure:
  """Returns a bolded version of the first figure.

  Args:
    subfigure: A value to render.
  """
  return figures_impl.TreescopeFigure(
      rendering_parts.custom_style(
          treescope_part_from_display_object(subfigure), "font-weight: bold"
      )
  )

