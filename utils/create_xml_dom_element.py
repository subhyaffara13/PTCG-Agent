
def create_xml_dom_element(
    doc: minidom.Document, name: str, value: Any
) -> minidom.Element:
  """Returns an XML DOM element with name and text value.

  Args:
    doc: minidom.Document, the DOM document it should create nodes from.
    name: str, the tag of XML element.
    value: object, whose string representation will be used
        as the value of the XML element. Illegal or highly discouraged xml 1.0
        characters are stripped.

  Returns:
    An instance of minidom.Element.
  """
  s = str(value)
  if isinstance(value, bool):
    # Display boolean values as the C++ flag library does: no caps.
    s = s.lower()
  # Remove illegal xml characters.
  s = _ILLEGAL_XML_CHARS_REGEX.sub('', s)

  e = doc.createElement(name)
  e.appendChild(doc.createTextNode(s))
  return e

