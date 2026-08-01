
def get_elem_value(elem, name):
  """Returns the value of XML element with the given name."""
  for child in elem:
    if child.attrib.get("name") != name:
      continue
    if child.tag == "string":
      return child.attrib.get("value")
    if child.tag == "boolean":
      return child.attrib.get("value") == "true"
    if child.tag == "list":
      return [nested_child.attrib.get("value") for nested_child in child]
    raise "Cannot recognize tag: " + child.tag
  return None

