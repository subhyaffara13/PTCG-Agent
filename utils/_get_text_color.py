
def _get_text_color(color: str) -> str:
    r, g, b = map(lambda x: int(x, 16), (color[1:3], color[3:5], color[5:7]))  # noqa: C417
    if (r * 0.299 + g * 0.587 + b * 0.114) > 186:
        return "#000000"
    return "#ffffff"


def _get_text_color(color: str) -> str:
  r, g, b = map(lambda x: int(x, 16), (color[1:3], color[3:5], color[5:7]))
  if (r * 0.299 + g * 0.587 + b * 0.114) > 186:
    return "#000000"
  return "#ffffff"

