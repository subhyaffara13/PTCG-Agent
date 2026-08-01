
def parse_rule(elem, package):
  """Returns a rule from bazel XML rule."""
  return Rule(
      type=elem.attrib["class"],
      name=get_elem_value(elem, "name"),
      package=package,
      srcs=normalize_paths(get_elem_value(elem, "srcs") or []),
      hdrs=normalize_paths(get_elem_value(elem, "hdrs") or []),
      textual_hdrs=normalize_paths(get_elem_value(elem, "textual_hdrs") or []),
      deps=get_elem_value(elem, "deps") or [],
      visibility=get_elem_value(elem, "visibility") or [],
      testonly=get_elem_value(elem, "testonly") or False)

