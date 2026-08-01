
def read_build(package):
  """Runs bazel query on given package file and returns all cc rules."""
  result = subprocess.check_output(
      ["bazel", "query", package + ":all", "--output", "xml"])
  root = xml.etree.ElementTree.fromstring(result)
  return [
      parse_rule(elem, package)
      for elem in root
      if elem.tag == "rule" and elem.attrib["class"].startswith("cc_")
  ]

