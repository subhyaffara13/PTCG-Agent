
def styled(subfigure: Any, style: str) -> figures_impl.TreescopeFigure:
  """Returns a CSS-styled version of the first figure.

  Args:
    subfigure: A value to render.
    style: A CSS style string.
  """
  return figures_impl.TreescopeFigure(
      rendering_parts.custom_style(
          treescope_part_from_display_object(subfigure), style
      )
  )

