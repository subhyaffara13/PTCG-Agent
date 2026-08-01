
def oklch_color(
    lightness: float, chroma: float, hue: float, alpha: float = 1.0
) -> str:
  """Constructs an OKLCH CSS color.

  See https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch and
  https://oklch.com/.

  Args:
    lightness: Lightness argument (0 to 1)
    chroma: Chroma argument (0 to 0.5 in practice; large values are clipped)
    hue: Hue argument (0 to 360)
    alpha: Opacity (0 to 1)

  Returns:
    A CSS color string.
  """
  return f"oklch({lightness} {chroma} {hue} / {alpha})"

