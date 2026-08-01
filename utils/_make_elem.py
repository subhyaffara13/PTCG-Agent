
def _make_elem(tag: str, *children: Element, **attrs) -> StaticDOMElement:
  """Helper function for making DOM elements."""
  return StaticDOMElement(tag, list(children), attrs)

