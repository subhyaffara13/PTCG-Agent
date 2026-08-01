
def _canonicalize_color(color: Color) -> str:
    if isinstance(color, str):
        return color
    r, g, b = (int(a * 255) for a in color)
    return f"#{r:02X}{g:02X}{b:02X}"


def _canonicalize_color(color: Color) -> str:
  if isinstance(color, str):
    return color
  r, g, b = (int(a * 255) for a in color)
  return f"#{r:02X}{g:02X}{b:02X}"

