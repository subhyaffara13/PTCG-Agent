import math


def text_on_color(
    text: str,
    value: float,
    vmax: float = 1.0,
    vmin: float | None = None,
    colormap: list[tuple[int, int, int]] | None = None,
) -> figures_impl.TreescopeFigure:
  """Renders some text on colored background, with the default colormap.

  Args:
    text: Text to display.
    value: Value to color the background with.
    vmax: Maximum value for the colormap.
    vmin: Minimum value for the colormap. Defaults to ``-vmax``.
    colormap: Explicit colormap to use. If not provided, uses the default
      diverging colormap if ``vmin`` is not provided, or the default sequential
      colormap if ``vmin`` is provided.

  Returns:
    A rendering of this word, formatted similarly to how this value would be
    formatted in an array visualization.
  """
  if colormap is None:
    if vmin is None:
      colormap = arrayviz.default_diverging_colormap.get()
    else:
      colormap = arrayviz.default_sequential_colormap.get()

  if vmin is None:
    vmin = -vmax

  if value > vmax:
    is_out_of_bounds = True
    color = colormap[-1]
  elif value < vmin:
    is_out_of_bounds = True
    color = colormap[0]
  else:
    is_out_of_bounds = False
    relative = (value - vmin) / (vmax - vmin)
    continuous_index = relative * (len(colormap) - 1)
    base_index = int(math.floor(continuous_index))
    offset = continuous_index - base_index
    if base_index == len(colormap) - 1:
      base_index -= 1
      offset = 1
    assert base_index < len(colormap) - 1
    color = [
        v0 * (1 - offset) + v1 * offset
        for v0, v1 in zip(colormap[base_index], colormap[base_index + 1])
    ]

  r, g, b = color
  # Logic matches `contrasting_style_string` in arrayviz.js
  # https://en.wikipedia.org/wiki/Grayscale#Colorimetric_(perceptual_luminance-preserving)_conversion_to_grayscale
  intensity = 0.2126 * r + 0.7152 * g + 0.0722 * b
  if intensity > 128:
    text_color = "black"
  else:
    text_color = "white"
  return figures_impl.TreescopeFigure(
      arrayviz_impl.ValueColoredTextbox(
          child=rendering_parts.text(text),
          text_color=text_color,
          background_color=f"rgb({r} {g} {b})",
          out_of_bounds=is_out_of_bounds,
          value=value,
      )
  )

