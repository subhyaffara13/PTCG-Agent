from typing import Any

def with_color(subfigure: Any, color: str) -> figures_impl.TreescopeFigure:
  """Returns a colored version of the first figure.

  Args:
    subfigure: A value to render.
    color: Any CSS color string.
  """
  return figures_impl.TreescopeFigure(
      rendering_parts.custom_style(
          treescope_part_from_display_object(subfigure), f"color: {color}"
      )
  )

