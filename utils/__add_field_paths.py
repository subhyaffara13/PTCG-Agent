
def _AddFieldPaths(node, prefix, field_mask):
  """Adds the field paths descended from node to field_mask."""
  stack = [(node, prefix)]
  while stack:
    current_node, current_prefix = stack.pop()
    if not current_node and current_prefix:
      field_mask.paths.append(current_prefix)
      continue
    for name in sorted(current_node, reverse=True):
      if current_prefix:
        child_path = current_prefix + '.' + name
      else:
        child_path = name
      stack.append((current_node[name], child_path))

