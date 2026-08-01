
def with_font_size(
    subfigure: Any, size: str | float
) -> figures_impl.TreescopeFigure:
  """Returns a scaled version of the first figure.

  Args:
    subfigure: A value to render.
    size: A multiplier for the font size (as a float) or a string giving a
      specific CSS font size (e.g. "14pt" or "2em").
  """
  if isinstance(size, str):
    style = f"font-size: {size}"
  else:
    style = f"font-size: {size}em"
  return figures_impl.TreescopeFigure(
      rendering_parts.custom_style(
          treescope_part_from_display_object(subfigure), style
      )
  )

