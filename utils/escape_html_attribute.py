
def escape_html_attribute(attribute: str) -> str:
  """Escapes a string for rendering in a HTML attribute."""
  return attribute.replace("&", "&amp;").replace('"', "&quot;")

