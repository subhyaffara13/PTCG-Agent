
def filter_terminal_infostates(infostates_map: InfostateMapping):
  """Filter out terminal infostate_node values."""
  return {
      infostate_string: infostate_node
      for infostate_string, infostate_node in infostates_map.items()
      if not infostate_node.is_terminal()
  }

