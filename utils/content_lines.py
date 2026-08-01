
def content_lines(lines):
  """Return lines with content."""
  return [line for line in lines if line and line[0] == "#"]

