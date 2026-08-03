import re

def format_source_location(
    filepath: str, lineno: int
) -> rendering_parts.RenderableTreePart:
  """Formats a reference to a given filepath and line number."""

  # Try to match it as an IPython file
  ipython_output_path = re.fullmatch(
      r"<ipython-input-(?P<cell_number>\d+)-.*>", filepath
  )
  if ipython_output_path:
    cell_number = ipython_output_path.group("cell_number")
    return rendering_parts.text(f"line {lineno} of output cell {cell_number}")

  return rendering_parts.text(f"line {lineno} of {filepath}")

