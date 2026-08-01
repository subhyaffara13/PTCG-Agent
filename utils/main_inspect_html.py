
def main_inspect_html(root: nodes.Node) -> str:
  """Main HTML content."""
  return H.ul(class_='tree-root')(root.header_html)

