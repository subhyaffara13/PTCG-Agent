
def get_inspect_html(id_: str) -> str:
  """Returns the inspect content."""
  node = nodes.Node.from_id(id_)
  return core.main_inspect_html(node)

