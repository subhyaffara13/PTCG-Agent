
def _escape_xml_attr(content):
  """Escapes xml attributes."""
  # Note: saxutils doesn't escape the quotes.
  return saxutils.escape(content, _escape_xml_attr_conversions)

