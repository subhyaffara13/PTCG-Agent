
def figure_from_treescope_rendering_part(
    part: rendering_parts.RenderableTreePart,
) -> figures_impl.TreescopeFigure:
  """Returns a figure object that displays a Treescope rendering part.

  Args:
    part: A Treescope rendering part to display, usually constructed via
      `repr_lib` or `rendering_parts`.

  Returns:
    A figure object that can be rendered in IPython.
  """
  return figures_impl.TreescopeFigure(part)

